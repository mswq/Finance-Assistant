from django.urls import path
from . import views

urlpatterns = [
    path ('add/', views.add_transaction, name ='add_transaction'),
    path ('dashboard/', views.dashboard, name='dashboard'),
    path ('add_category/', views.add_category, name='add_category'),
    path ('goals/', views.goals, name='goals')
]