from django.shortcuts import render, redirect

# Create your views here.

#피드페이지
def feeds(request):
    #유저정보를 갖고와서 로그인 여부를 확인
    user = request.user
    is_authenticated = user.is_authenticated

    if not request.user.is_authenticated:
        return redirect('/users/login/')

    print('user: ', user)
    print('is_authenticated: ', is_authenticated)

    return render(request, 'posts/feeds.html')

