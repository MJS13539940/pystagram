from django.db import models

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('users.User', verbose_name='작성자', on_delete=models.CASCADE) #User클래스를 대상으로 외부키를 적용
    content = models.TextField('내용')
    created = models.DateTimeField('생성일시', auto_now_add=True) #자동으로 현재시각을 추가
    tags = models.ManyToManyField('posts.HashTag', verbose_name='해시태그 목록', blank=True)
                # 아래에 선언해서 참조 못할땐 문자열로 경로를 가르쳐준다.

class PostImage(models.Model):
    post = models.ForeignKey(Post, verbose_name='포스트', on_delete=models.CASCADE)
    photo = models.ImageField('사진', upload_to='post')


class Comment(models.Model):
    user = models.ForeignKey('users.User', verbose_name='작성자', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='포스트', on_delete=models.CASCADE)
    content = models.TextField('내용')
    created = models.DateTimeField('생성일시', auto_now_add=True)

class HashTag(models.Model):
    name = models.CharField('태그명', max_length=50)
    #문자열을 돌려보내줌
    def __str__(self):
        return self.name