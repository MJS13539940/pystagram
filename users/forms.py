# 폼을 작성해 나중에 호출
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget = forms.TextInput(
            attrs={'placeholder': '사용자명 (3자리 이상)'},
        ),
        )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput( #입력한 비밀번호를 *로 보이게도 해줌
            attrs={'placeholder': '비밀번호 (4자리 이상)'},
        ),
        )
    
#회원가입용 양식
class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    profile_image = forms.ImageField()
    short_description = forms.CharField()


