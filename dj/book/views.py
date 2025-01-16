import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from main.models import Post, WiseUser


def book(request):
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

        return redirect(reverse('book:book'))
    
    if request.method == "PATCH":
        data = json.loads(request.body)
        post = Post.published.get(id=data.get('post_id'))
        user = WiseUser.objects.get(id=data.get('user_id'))

        post.accepted.remove(user)
        post.save()

        response_data = {'status': '200'}
        return JsonResponse(response_data)
    
    user_id = request.user.id
    posts1 = Post.objects.filter(accepted__id=user_id)
    posts2 = Post.objects.filter(author__id=user_id)
    posts = posts1 | posts2
    
    context = {'posts': posts,}

    return render(request, 'book/book.html', context=context,)
