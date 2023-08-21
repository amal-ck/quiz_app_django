from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.master_register, name='master_register'),
    path('accounts/login/', views.master_login, name='master_login'),
    path('', views.dash, name='dash'),
    path('accounts/logout/', views.master_logout, name='master_logout'),
    path('add_question/<int:quiz_id>', views.add_question, name='add_question'),
    path('edit_question/<int:question_id>', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>', views.remove_question, name='delete_question'),
    path('add_quiz', views.add_quiz, name='add_quiz'),
    path('edit_quiz/<int:quiz_id>', views.edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:quiz_id>', views.remove_quiz,name='delete_quiz')
]