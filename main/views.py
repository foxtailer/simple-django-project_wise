import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from main.forms import UserLoginForm, UserRegistrationForm

from .models import Post, WiseUser


def home(request):
    context = {
        'page_title': 'Wise',
    }
    return render(request, 'main/home.html', context=context)


def write(request):
    if request.method == "POST":
        text = request.POST.get('text')
        answer = bool(request.POST.get('answer'))
        status = bool(request.POST.get('status'))
        user_id = request.user.id
        
        user = WiseUser.objects.get(id=user_id)

        Post.objects.create(text=text,
                            author=user,
                            reply=answer,
                            status=Post.Status.PUBLISHED if status else Post.Status.DRAFT)
    
    return render(request, 'main/write.html')


def my(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        post_id = data.get('post_id')

        post = Post.objects.get(id=post_id)
        post.delete()

        response_data = {
            'id': post_id,
        }

        return JsonResponse(response_data)
    
    if request.method == "POST":
        text = request.POST.get('text')
        answer = bool(request.POST.get('answer'))
        status = bool(request.POST.get('status'))
        post_id = request.POST.get('post_id')

        post = Post.objects.get(id=post_id)
        post.text = text
        post.answer = answer
        post.status = Post.Status.PUBLISHED if status else Post.Status.DRAFT
        post.save()

        return redirect(reverse('main:my'))
    
    user_id = request.user.id
    posts1 = Post.objects.filter(accepted__id=user_id)
    posts2 = Post.objects.filter(author__id=user_id)
    posts = posts1 | posts2
    
    context = {'posts': posts,}

    return render(request,
                  'main/my.html',
                  context=context,)


@require_POST
def report(request):
    post_id = request.POST.get('post_id')
    user = request.user
    try:
        wisdom = Post.published.get(id=post_id)
        wisdom.report += 1
        wisdom.reported_by.add(user)
        wisdom.save()
        return JsonResponse({'status': 'success', 'report': wisdom.report})
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Wisdom not found'}, status=404)


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
