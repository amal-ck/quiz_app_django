from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from quiz_master.models import QuizModel
import  datetime
from django.http import JsonResponse

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='users')
            user.groups.add(user_group)
            return redirect('login') 
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.groups.filter(name='users').exists():
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect('home')
            else:
                form.add_error(None, "Invalid Username or Password, Please Try again")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  

@login_required
def home(request):
    if request.user.groups.filter(name='users').exists():
       context = {
           'user' : request.user,
           'show_navbar' : True
       }
       return render(request, 'home.html', context)
    else:
        return redirect('login')
    
@login_required
def quiz(request):
    if request.user.groups.filter(name='users').exists():
        question_index = request.session.get('question_index', 0)
        if 'start_time' not in request.session:
            request.session['start_time'] = str(datetime.datetime.now())

        start_time = datetime.datetime.strptime(request.session['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.datetime.now()
        time_elapsed = current_time - start_time

        countdown_seconds = 30  

        if time_elapsed.total_seconds() < countdown_seconds:
            time_remaining = countdown_seconds - time_elapsed.total_seconds()
            minutes = int(time_remaining // 60)
            seconds = int(time_remaining % 60)
            time_remaining_display = f'{minutes}:{seconds:02}'
        else:
            time_remaining_display = '0:00'

        try:
            question = QuizModel.objects.all()[question_index]
        except IndexError:
            question = None

        total_questions = QuizModel.objects.count()

        context = {
            'question': question,
            'question_index': question_index,
            'total_questions': total_questions,
            'show_navbar': True,
            'time_remaining':time_remaining_display
        }
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
             return JsonResponse({'time_remaining': time_remaining_display})
        
        return render(request, 'quiz.html', context)

@login_required
def next_question(request):
    if request.method == 'POST' and request.user.groups.filter(name='users').exists():
        question_index = request.session.get('question_index', 0)
        selected_choice = request.POST.get('selected_choice')
        try:
            question = QuizModel.objects.all()[question_index]
        except IndexError:
            question = None
        if question and selected_choice == question.ans:
            request.session.setdefault('correct_count', 0)
            request.session['correct_count'] += 1
        else:
            request.session.setdefault('incorrect_count', 0)
            request.session['incorrect_count'] += 1

        question_index += 1
        request.session['question_index'] = question_index

        if question_index < QuizModel.objects.count():
            return redirect('quiz')
        else: 
            if 'end_time' not in request.session:
               request.session['end_time'] = str(datetime.datetime.now())
        return redirect('quiz_results')
    
    return redirect('quiz')

@login_required
def quiz_results(request):
    if request.user.groups.filter(name='users').exists():
        correct_count = request.session.get('correct_count', 0)
        incorrect_count = request.session.get('incorrect_count', 0)
        total_questions = QuizModel.objects.count()
        answered_questions = request.session.get('question_index', 0) + 1
        

        if answered_questions < total_questions and answered_questions != 1 :
            return redirect('quiz')
        if answered_questions != 1:
                start_time_str = request.session.get('start_time')
                start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
                end_time_str = request.session.get('end_time')
                end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
                time_taken = end_time - start_time
                total_seconds = time_taken.total_seconds()
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
        else:
                minutes = seconds = 0 

        context = {
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'total_questions': total_questions,
            'show_navbar': True,
            'minutes':minutes,
            'seconds':seconds
        }
        return render(request, 'result.html', context)
    
@login_required
def restart_quiz(request):
    request.session.pop('question_index', None)  # Remove session variable
    request.session.pop('correct_count', None)   
    request.session.pop('incorrect_count', None)
    request.session.pop('answered_questions', None)
    request.session.pop('start_time', None)
    request.session.pop('end_time', None)
    return redirect('quiz')