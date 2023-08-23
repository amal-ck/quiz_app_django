from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('next_question/<int:quiz_id>/', views.next_question, name='next_question'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
]