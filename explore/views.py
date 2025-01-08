import json

from django.shortcuts import render
from django.http import JsonResponse, Http404

from main.models import Post, WiseUser


def explore(request):
    user_id = request.user.id

    # When klick next button
    if request.method == "POST":
        except_id = request.POST.get('wisdom_id')
        user = WiseUser.objects.get(id=user_id)
        post = Post.random_wisdome(except_id, user_id)

        response_data = {
            'wisdom': post.text,
            'wisdom_id': post.id,
            'reply': post.reply if post.author != user else False,
            'email': post.author.email,
            'is_accepted': post.accepted.filter(id=user.id).exists(),
        }

        return JsonResponse(response_data)

    elif request.method == "PATCH":
        data = json.loads(request.body)

        post = Post.published.get(id=data.get('post_id'))
        user = WiseUser.objects.get(id=data.get('user_id'))
        is_accepted = data.get('is_accepted') == 'True' or data.get('is_accepted')

        if is_accepted:
            post.accepted.remove(user)
            post.save()
        else:
            post.accepted.add(user)
            post.save()

        response_data = {'status': '200',
                         'is_accepted': not is_accepted}
        return JsonResponse(response_data)
    
    elif request.method == "PUT":
        data = json.loads(request.body)

        post = Post.published.get(id=data.get('post_id'))
        user = WiseUser.objects.get(id=data.get('user_id'))
        
        post.report += 1
        post.reported_by.add(user)
        post.save()

        response_data = {'status': '200',}
        return JsonResponse(response_data)
    
    try:
        post = Post.random_wisdome(user=user_id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")
    
    context = {
        'page_title': 'Explore',
        'post': post,
        'is_accepted': post.accepted.filter(id=user_id).exists(),
    }

    return render(request, 'explore/explore.html', context=context)
