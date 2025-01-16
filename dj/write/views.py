from django.shortcuts import render

from main.models import WiseUser, Post


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
    
    return render(request, 'write/write.html')
