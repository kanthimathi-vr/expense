

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.dashboard_view, name='dashboard'),

    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/create/', views.expense_create_view, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update_view, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),

    path('admin-view/', views.admin_view, name='admin_view'),
]
