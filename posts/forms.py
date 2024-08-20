#댓글 쓰기위한 폼을 구현
from django import forms

from posts.models import Comment

#폼을 위한 클래스
class CommentForm(forms.ModelForm):
    #메다데이터
    class Meta:
        model = Comment
        fields = [
            'user', 
            'post', 
            'content', 
        ]
