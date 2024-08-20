from django.shortcuts import render, redirect
from posts.models import Post

# Create your views here.

#피드페이지
def feeds(request):
    #유저정보를 갖고와서 로그인 여부를 확인
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    #Post 의 내용을 받아와서 피드 페이지에 렌더링해서 표시한다.
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/feeds.html', context)

