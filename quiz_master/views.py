from django.shortcuts import render, redirect, get_object_or_404
from .forms import MasterRegistrationForm, MasterLoginForm, QuizForm, QuestionForm  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import QuizModel, QuestionModel
from django.urls import reverse
from django.db.models import Count

def master_register(request):
    if request.method == 'POST':
        form = MasterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            masters_group = Group.objects.get(name='masters')
            user.groups.add(masters_group)
            return redirect('master_login') 
    else:
            form = MasterRegistrationForm()
            
    return render(request, 'master_signup.html', {'form':form, 'master':True})

def master_login(request):
    if request.method == 'POST':
        form = MasterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.groups.filter(name='masters').exists():
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect('dash')
            else:
                form.add_error(None, "Invalid Username or Password, Please Try again")
    else:
        form = MasterLoginForm()

    return render(request, 'master_login.html', {'form':form, 'master':True})

def master_logout(request):
    logout(request)
    return redirect('master_login')  

@login_required(login_url='master_login')
def dash(request):
    if request.user.groups.filter(name='masters').exists():
        quizzes = QuizModel.objects.annotate(total_questions=Count('questionmodel'))
        context = {
            'quiz_list' : quizzes,
            'show_navbar' : True,
            'master' : True
        }
        return render(request, 'dash.html', context)
    else:
        return redirect('master_login')

@login_required
def add_question(request,quiz_id):
    if request.user.groups.filter(name='masters').exists():
       quiz = get_object_or_404(QuizModel, pk=quiz_id)
       if request.method == 'POST':
           form = QuestionForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect(reverse('edit_quiz', args=[quiz_id]))
       else:
           initial_data = {'quiz': quiz}
           form = QuestionForm(initial=initial_data)
           
           context = {
               'form' : form,
               'quiz_id':quiz_id,
               'show_navbar' : True,
               'master':True
           }
   
       return render(request, 'questions.html', context)
    else:
        return redirect('master_login')
    
@login_required
def edit_question(request, question_id):
    if request.user.groups.filter(name='masters').exists():
       question = get_object_or_404(QuestionModel, pk=question_id)
   
       if request.method == 'POST':
           form = QuestionForm(request.POST, instance=question)
           if form.is_valid():
               form.save()
               return redirect(reverse('edit_quiz', args=[question.quiz_id]))
   
       else:
           context = {
               'form' : QuestionForm(instance=question),
               'show_navbar' : True,
               'question_id' : question_id,
               'master':True
           }
   
       return render(request, 'edit.html', context)
    else:
        return redirect('master_login')

@login_required
def remove_question(request,question_id):
    if request.user.groups.filter(name='masters').exists():
        question = QuestionModel.objects.get(pk = question_id)
        question.delete()
        return redirect(reverse('edit_quiz', args=[question.quiz_id]))
    else:
        return redirect('master_login')
@login_required    
def add_quiz(request):
    if request.user.groups.filter(name='masters').exists():
        context = {
            'show_navbar': True,
            'master': True
        }
        if request.method == 'POST':
            form = QuizForm(request.POST)
            if form.is_valid():
                form.save()
                print("Form is valid, redirecting to dash")
                return redirect('dash')
        else:
            context['form'] = QuizForm()

        return render(request, 'add_quiz.html', context)
    else:
        return redirect('master_login')
@login_required
def edit_quiz(request, quiz_id):
    if request.user.groups.filter(name='masters').exists():
       quiz = get_object_or_404(QuizModel, pk=quiz_id)
   
       if request.method == 'POST':
           form = QuizForm(request.POST, instance=quiz)
           if form.is_valid():
               form.save()
               return redirect('dash')
   
       else:
           question = QuestionModel.objects.filter(quiz_id = quiz_id)
           context = {
               'form' : QuizForm(instance=quiz),
               'questions' : question,
               'show_navbar' : True,
               'quiz_id' : quiz_id,
               'master':True
           }
   
       return render(request, 'edit_quiz.html', context)
    else:
        return redirect('master_login')
    
@login_required
def remove_quiz(request,quiz_id):
    if request.user.groups.filter(name='masters').exists():
        quiz = QuizModel.objects.get(pk = quiz_id)
        quiz.delete()
        return redirect('dash')
    else:
        return redirect('master_login')