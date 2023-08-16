from django.shortcuts import render, redirect
from .forms import MasterRegistrationForm, MasterLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def master_register(request):
    if request.method == 'POST':
        form = MasterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            masters_group = Group.objects.get(name='masters')
            user.groups.add(masters_group)
            return redirect('login') 
    else:
        form = MasterRegistrationForm()

    return render(request, 'master_signup.html', {'form': form})

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

    return render(request, 'master_login.html', {'form': form})

def master_logout(request):
    logout(request)
    return redirect('master_login')  

@login_required(login_url='master_login')
def dash(request):
    if request.user.groups.filter(name='masters').exists():
       navbar = True
       return render(request, 'dash.html', {'show_navbar':navbar})
    else:
        return redirect('master_login')
    
