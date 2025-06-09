from django import forms
from .models import Transaction, Category, UserProfile

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta: 
        model = Category
        fields =['name']

class GoalForm(forms.ModelForm):
    class Meta: 
        model = UserProfile
        fields = ['goal']