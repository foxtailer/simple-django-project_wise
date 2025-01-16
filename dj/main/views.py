from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main.forms import UserLoginForm, UserRegistrationForm


def home(request):
    context = {
        'page_title': 'Wise',
    }
    return render(request, 'main/home.html', context=context)


def registration(request):
  if request.method == 'POST':
    form = UserRegistrationForm(data=request.POST)
    if form.is_valid():
      form.save()
      user = form.instance
      auth.login(request, user)
      return redirect(reverse('main:home'))
  else:
    form = UserRegistrationForm()

  context = {
    'form': form,
  }

  return render(request, 'main/registration.html', context)


def login(request):
  form = UserLoginForm(data=request.POST)
  if form.is_valid():
    username = request.POST['username']  
    password = request.POST['password']  
      
    user = auth.authenticate(username=username, password=password)
    if user:
      auth.login(request, user)
      fail = False
      return redirect(reverse('main:home'))
    
  fail = True
    
  context = {
    'fail': fail,
    'form': form,
  }

  return render(request, 'main/main.html', context)


@login_required
def logout(request):
  auth.logout(request)
  return redirect(reverse('main:home'))
