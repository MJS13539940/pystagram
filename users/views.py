from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import LoginForm, SignupForm
from users.models import User
# Create your views here.

def login_view(request):
    #로그인 되어있으면 피드로 보냄
    if request.user.is_authenticated:
        return redirect('posts:feeds')
    

    #로그인 되어있지 않으면+요청형식이 포스트일경우
    if request.method == 'POST':
        form = LoginForm(data=request.POST) #리퀘스트 정보 중 포스트에 해당하는게 폼에 들어감
        #print('form.is_valid(): ', form.is_valid())
        #print('form.cleaned_data():', form.cleaned_data())

        if form.is_valid():#이러한 과정으로 인증거치기
            username = form.cleaned_data['username'] #유저네임을 읽어와서 집어넣기
            password = form.cleaned_data['password'] 
            user = authenticate(username=username, password=password)

            if user: #user가 비어있지 않다면
                login(request, user)
                return redirect('posts:feeds')
            else:
                form.add_error(None, '입력한 자격증명에 해당하는 사용자가 없습니다.') #제목은 None인 해당하는 에러를 추가함.
                print('로그인에 실패했습니다.')
    
    else: #리퀘스트가 post가 아닌경우
        form = LoginForm()
        context = {'form': form,}

    #로그인 페이지로 돌아감
    context = {'form': form,}
    return render(request, 'users/login.html', context)


#로그아웃용 뷰(템플릿 필요없음)
def logout_view(request):
    logout(request)
    return redirect('users:login')



#회원가입
def signup(request):
    #POST형태의 요청인지 확인
    if request.method == 'POST':
        form = SignupForm(data=request.POST, files=request.FILES)

        #form 정상인지 확인
        if form.is_valid():
            #유저정보 저장 후 로그인, feed화면으로 보냄.
            user = form.save()
            login(request, user)
            return redirect('posts:feeds') #로그인하면 피드화면으로 보냄

    else:    
        form = SignupForm()

    #결과적으로 로그인하지 않을경우 회원가입 페이지로 다시 보냄
    context = {'form': form}
    return render(request, 'users/signup.html', context)

def profile(request, user_id):
    return render(request, "users/profile.html")

# 프로필 Template에 정보 전달
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
    }

    return render(request, 'users/profile.html', context)

# 팔로워
def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/followers.html", context)

# 팔로잉
def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/following.html", context)

#팔로우 토글
def follow(request, user_id): #왼쪽은 사용자정보, 오른쪽은 대상정보가 될것임
    #로그인 한 유저
    user = request.user
    #팔로우 하려는 유저
    target_user = get_object_or_404(User, id=user_id)

    # 팔로우 하려는 유저가 이미 자신의 팔로잉 목록에 있는 경우
    if target_user in user.following.all():
        # 팔로잉 목록에서 제거
        user.following.remove(target_user)

    # 팔로우 하려는 유저가 자신의 팔로잉 목록에 없는 경우
    else:
        # 팔로잉 목록에 추가
        user.following.add(target_user)

    # 팔로우 토글 후 이동할 URL이 전달되었다면 해당 주소로,
    # 전달되지 않았다면 로그인 한 유저의 프로필 페이지로 이동
    url_next = request.GET.get("next") or reverse("users:profile", args=[user.id])
    return HttpResponseRedirect(url_next)

