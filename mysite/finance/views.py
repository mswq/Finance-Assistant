from django.shortcuts import render, redirect
from .form import TransactionForm, CategoryForm, BalanceForm
from .models import Transaction, Category, UserProfile
from collections import defaultdict
import matplotlib.pyplot as plt
import base64
from datetime import date, timedelta
import io

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else: 
        form = TransactionForm(user=request.user)
    return render(request, 'finance/add_transaction.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('add_transaction')
    else: 
        form = CategoryForm()
    return render(request, 'finance/add_category.html', {'form': form})

# To do: make this only an option in login?
def update_balance(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else: 
        form = BalanceForm(instance=profile)
    return render(request, 'finance/update_balance.html', {'form': form})

def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    view_range = request.GET.get('range', 'all')
    today = date.today()

    if view_range == "week":
        start_date = today - timedelta(days=7)
    elif view_range == "month":
        start_date = today.replace(day=1)
    else:
        start_date = None

    if start_date:
        transactions = Transaction.objects.all().filter(user=request.user, date__gte=start_date)
    else:
        transactions = Transaction.objects.all().filter(user=request.user)

    current_balance = profile.balance
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = current_balance if current_balance != 0 else income - expense

    # Income vs Expense bar graph
    labels = ['Income', "Expense"]
    values = [income, expense]
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Income vs Expense Bar Graph')
    plt.xlabel('Transaction')
    plt.ylabel('Amount')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    bar_graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Category pie chart
    category_totals = {}

    for t in transactions:
        if t.category:
            cat_name = t.category.name
        else:
            continue
        if cat_name not in category_totals:
            category_totals[cat_name] = float(t.amount)
        else: 
            category_totals[cat_name] += float(t.amount)

    p_labels = list(category_totals.keys())
    p_values = list(category_totals.values())

    plt.pie(p_values, labels=p_labels, startangle=90)
    plt.title('Category Pie Chart')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    pie_graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'finance/dashboard.html', {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
        'graph': bar_graph_base64,
        'pie_graph': pie_graph_base64,
        'view_range': view_range
    })