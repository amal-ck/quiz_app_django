from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.master_register, name='master_register'),
    path('accounts/login/', views.master_login, name='master_login'),
    path('', views.dash, name='dash'),
    path('accounts/logout/', views.master_logout, name='master_logout'),
]