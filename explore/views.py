import json

from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.core.serializers import serialize

from main.models import Post, WiseUser


def explore(request):
    user_id = request.user.id

    # When klick next button
    if request.method == "POST":
        except_id = request.POST.get('wisdom_id')
        if user_id:
            user = WiseUser.objects.get(id=user_id)
            post = Post.random_wisdome(except_id, user_id)
        else:
            post = Post.random_wisdome(except_id)
        post_data = serialize('json', [post])

        response_data = {
            'wisdom': post.text,
            'wisdom_id': post.id,
            'reply': False if not user_id else post.reply if post.author != user else False,
            'email': post.author.email,
            'is_accepted': 0 if not user_id else int(post.accepted.filter(id=user.id).exists()),
            'post': post_data,
        }

        return JsonResponse(response_data)

    # bookmark button
    elif request.method == "PATCH":
        print(request.body.decode('utf-8'))
        data = json.loads(request.body)
        print(data)

        post = Post.published.get(id=data.get('post_id'))
        user = WiseUser.objects.get(id=data.get('user_id'))
        is_accepted = True if int(data.get('is_accepted')) else False

        if is_accepted:
            post.accepted.remove(user)
            post.save()
        else:
            post.accepted.add(user)
            post.save()

        response_data = {'status': '200',
                         'is_accepted': not int(is_accepted)}
        return JsonResponse(response_data)
    
    # report
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
        'is_accepted': int(post.accepted.filter(id=user_id).exists()),
    }

    return render(request, 'explore/explore.html', context=context)


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
