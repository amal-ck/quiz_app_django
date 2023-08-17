from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('quiz/', views.quiz, name='quiz'),
    path('next_question/', views.next_question, name='next_question'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('restart_quiz/', views.restart_quiz, name='restart_quiz'),
]