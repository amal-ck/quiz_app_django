from django.shortcuts import render, redirect, get_object_or_404
from .forms import MasterRegistrationForm, MasterLoginForm, QuizForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import QuizModel

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
        context = {
            'questions' : QuizModel.objects.all(),
            'show_navbar' : True,
            'master' : True
        }
        return render(request, 'dash.html', context)
    else:
        return redirect('master_login')

@login_required
def add_question(request):
    if request.user.groups.filter(name='masters').exists():
       if request.method == 'POST':
           form = QuizForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('dash')
       else:
           
           context = {
               'form' : QuizForm(),
               'show_navbar' : True,
               'master':True
           }
   
       return render(request, 'questions.html', context)
    else:
        return redirect('master_login')
    
@login_required
def edit_question(request, question_id):
    if request.user.groups.filter(name='masters').exists():
       question = get_object_or_404(QuizModel, pk=question_id)
   
       if request.method == 'POST':
           form = QuizForm(request.POST, instance=question)
           if form.is_valid():
               form.save()
               return redirect('dash')
   
       else:
           context = {
               'form' : QuizForm(instance=question),
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
        question = QuizModel.objects.get(pk = question_id)
        question.delete()
        return redirect('dash')
    else:
        return redirect('master_login')