from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/', views.user_logout, name='logout'),
]