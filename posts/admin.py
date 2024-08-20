from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget ##
from django.db import models                              # admin 썸네일 추가때 씀 
from django.utils.safestring import mark_safe            ##

import admin_thumbnails

from posts.models import Post, PostImage, Comment

# Register your models here.

#포스트 안에 넣을 수 있게 함.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

# AdminFileWidget은 관리자 페이지에서 '파일 선택' 버튼을 보여주는 부분
# 이 widget을 커스텀하여 <img> 태그를 추가함
class InlineImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer) #부모클래스의 render를 호출
        # 값이 비어있지 않음 and attr를 읽어올 때 value
        if value and getattr(value, 'url', None):
            html = mark_safe(f'<img src="{value.url}" width="150" height="150">') + html        
        return html

#포스트 안에 넣을 수 있게 함.
# @admin_thumbnails.thumbnail("photo") #썸네일 대상을 photo로 한다.(아래 주석처리한 부분의 기능을 데코레이터로 대체함)
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    # ImageField를 표시할 때, AdminFileWidget을 커스텀한 InlineImageWidget을 사용함
    formfield_overrides = {
        models.ImageField: {
            'widget': InlineImageWidget,
        }
    }


# 만들었던 모델 3가지를 admin에 추가
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content',]
    # 포스트 내에 두 내용이 포함된다.
    inlines = [CommentInline, PostImageInline,]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'photo',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'content',]

