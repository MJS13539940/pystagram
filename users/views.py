from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from users.forms import LoginForm, SignupForm
# Create your views here.

def login_view(request):
    #로그인 되어있으면 피드로 보냄
    if request.user.is_authenticated:
        return redirect('/posts/feeds/')
    

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
                # return redirect('/posts/feeds')
            else:
                form.add_error(None, '입력한 자격증명에 해당하는 사용자가 없습니다.') #제목은 None인 해당하는 에러를 추가함.
                print('로그인에 실패했습니다.')

        context = {'form': form,}
        return render(request, 'users/login.html', context)
    
    else: #리퀘스트가 post가 아닌경우
        form = LoginForm()
        context = {'form': form,}

        return render(request, 'users/login.html', context)


#로그아웃용 뷰(템플릿 필요없음)
def logout_view(request):
    logout(request)
    return redirect('/users/login/')



#회원가입
def signup(request):
    #POST형태의 요청인지 확인
    if request.method == 'POST':
        #
        form = SignupForm(data=request.POST, files=request.FILES)
        #form 정상인지 확인
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            profile_image = form.cleaned_data['profile_image']
            short_description = form.cleaned_data['short_description']

            #잘 나왔는지 확인
            print(username)
            print(password1, password2)
            print(profile_image)
            print(short_description)

            #유저정보 저장 후 로그인, feed화면으로 보냄.
            user = form.save()
            login(request, user)
            return redirect('/posts/feeds')

        #확인용
        #print(request.POST)
        #print(request.FILES) #이미지 정보 등

        context = {'form': form}
        return render(request, 'users/signup.html', context)

    form = SignupForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)


