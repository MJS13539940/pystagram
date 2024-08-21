#댓글 쓰기위한 폼을 구현
from django import forms

from posts.models import Comment, Post

#댓글폼을 위한 클래스
class CommentForm(forms.ModelForm):
    #메다데이터
    class Meta:
        model = Comment
        fields = [
            # 'user', (이부분이 있으면 댓글 입력시 필수항목이 비게 되어 ValueError가 뜸.)
            'post', 
            'content', 
        ]
        #위젯 추가
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "댓글 달기...",}
            )
        }


#글쓰기 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            # 'user', 사용자정보는 필드에 없어도 직접 확인함.
            'content',
        ]
