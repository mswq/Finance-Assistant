from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Logic: This class extends 'CreateView' and sets the form as  'UserCreationForm' and uses the signup template
# - reverse_lazy is used to redirect the users to the login page

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'