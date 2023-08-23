from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from quiz_master.models import QuizModel, QuestionModel
import  datetime
from django.db.models import Count
from .models import Results
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
       quizzes = QuizModel.objects.annotate(total_questions=Count('questionmodel'))
       context = {
           'quizzes' : quizzes,
           'user' : request.user.username,
           'show_navbar' : True
       }
       return render(request, 'home.html', context)
    else:
        return redirect('login')
    
@login_required
def quiz(request,quiz_id):
    if request.user.groups.filter(name='users').exists():
        question_index = request.session.get('question_index', 0)
        quiz = QuizModel.objects.filter(pk=quiz_id)
        for i in quiz:
            time = i.time
        if 'start_time' not in request.session:
            request.session['start_time'] = str(datetime.datetime.now())

        start_time = datetime.datetime.strptime(request.session['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        quiz_start_time = datetime.datetime.strptime(request.session['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        quiz_duration = datetime.timedelta(seconds=time)
        quiz_end_time = quiz_start_time + quiz_duration
        question = QuestionModel.objects.filter(quiz_id=quiz_id)
        total_questions = question.count()
        try:
            question = QuestionModel.objects.filter(quiz_id=quiz_id)[question_index]
        except IndexError:
            question = None

        context = {
            'total_questions':total_questions,
            'question': question,
            'question_index': question_index,
            'show_navbar': True,
            'quiz_id':quiz_id,
            'time': time,
            'quiz_end_time': quiz_end_time,
        }
        
        return render(request, 'quiz.html', context)

@login_required
def next_question(request, quiz_id):
    if request.user.groups.filter(name='users').exists():
        question_index = request.session.get('question_index', 0)
        question = QuestionModel.objects.filter(quiz_id=quiz_id)
        selected_choice = request.POST.get('selected_choice')
        
        request.session.setdefault('skipped_count', 0)
        request.session.setdefault('correct_count', 0)
        request.session.setdefault('incorrect_count', 0)
        if selected_choice is None:
            request.session['skipped_count'] += 1 
        elif selected_choice == question[question_index].ans:
            request.session['correct_count'] += 1
        else:
            request.session['incorrect_count'] += 1

        if question_index < question.count() - 1:
            request.session['question_index'] = question_index + 1
            return redirect(quiz, quiz_id=quiz_id)
        else: 
            if 'end_time' not in request.session:
               request.session['end_time'] = str(datetime.datetime.now())
            start_time_str = request.session.get('start_time')
            start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
            end_time_str = request.session.get('end_time')
            end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
            time_taken = end_time - start_time
            total_seconds = time_taken.total_seconds()

            quiz_instance = QuizModel.objects.get(pk=quiz_id)
            user = request.user
            results = Results(
                quiz=quiz_instance,
                quiz_user=user,
                correct_answers=request.session.get('correct_count'),
                incorrect_answers=request.session.get('incorrect_count'),
                skipped_answers=request.session.get('skipped_count'),
                total_time_taken=total_seconds
            )
            results.save()        
            del request.session['question_index']
            del request.session['start_time']
            del request.session['end_time']
            del request.session['correct_count']
            del request.session['incorrect_count']
            del request.session['skipped_count']
        return redirect('quiz_results')
            
    return redirect('quiz', quiz_id=quiz_id)

@login_required
def quiz_results(request):
    if request.user.groups.filter(name='users').exists():
        results = Results.objects.filter(quiz_user_id=request.user)
        formatted_results = []
        for result in results:
            total_seconds = result.total_time_taken
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)

            total_questions = result.correct_answers + result.incorrect_answers + result.skipped_answers
            score = f'{result.correct_answers} / {total_questions}'
            formatted_result = {
                'quiz': result.quiz,
                'score': score,
                'total_questions': total_questions,
                'correct_answers': result.correct_answers,
                'incorrect_answers': result.incorrect_answers,
                'skipped_answers': result.skipped_answers,
                'minutes': minutes,
                'seconds': seconds
            }
            formatted_results.append(formatted_result)
        
        context = {
            'show_navbar': True,
            'results': formatted_results
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