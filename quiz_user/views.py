from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='users')
            user.group.add(user_group)
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
       return render(request, 'home.html')
    else:
        return redirect('login')