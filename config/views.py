##### 첫 페이지 구성 #####
from django.shortcuts import render, redirect

#인덱스페이지를 반환하도록함.
def index(request):
    #로그인 되어 있다면 보내는 페이지
    if request.user.is_authenticated:
        return redirect('/posts/feeds/')
    else:
        return redirect('/users/login')

