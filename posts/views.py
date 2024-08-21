from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm

# Create your views here.

#피드페이지
def feeds(request):
    #유저정보를 갖고와서 로그인 여부를 확인
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    #Post 의 내용을 받아와서 피드 페이지에 렌더링해서 표시한다.
    posts = Post.objects.all()
    #글과 같이 보여줄 댓글창을 불러옴
    comment_form = CommentForm
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/feeds.html', context)


# 댓글을 실제로 추가할 수 있게하는 기능
@require_POST # POST의 내용을 요구하는 데코레이터. 여기선 POST의 내용을 받아 comment_add에 전달해준다
def comment_add(request):
    # print(request.POST)

    # 받아온 데이터를 이용해서 폼을 생성
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # 유저정보를 자동으로 들어가게함(댓글쓸 때 누가 어느 글에 댓글을 달건지 일일이 설정하지 않게 하는 과정)
        comment.user = request.user
        comment.save()

        print(comment.id)
        print(comment.content)
        print(comment.user)
        # HttpResponseRedirect 를 이용해 post.id를 찾아서 원하는 포스트 위치로 가게함.(댓글 쓰고나면 쓴 글이 바로 보이게 하려고)    
        # 동적 url 적용할 때 reverese 써야할 때도 있다.(?)
        url_next = reverse('posts:feeds') + f'#post-{comment.post.id}'
        return HttpResponseRedirect(url_next)
        # return HttpResponseRedirect(f'/posts/feeds/#post-{comment.post.id}')
    
    else:
        return redirect('/posts/feeds/')
    
# GET 메서드를 막음으로서 url을 통한 해킹을 막을 수 있다.
@require_POST
def comment_delete(request, comment_id): #삭제할땐 어느 댓글인지 알려줄 필요가 있다
    comment = Comment.objects.get(id=comment_id) #
    # 삭제해도 되는 사용자인지 확인
    if comment.user == request.user:
        comment.delete()
        url_next = reverse('posts:feeds') + f'#post-{comment.post.id}'
        return HttpResponseRedirect(url_next)
        # return HttpResponseRedirect(f'/posts/feeds/#post-{comment.post.id}')
    else:
        return HttpResponseForbidden('이 댓글을 삭제할 권한이 없습니다.')


#글쓰기 기능
def post_add(request):
    if request.method == 'POST':        
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # 이미지들은 따로 입력
            for image_file in request.FILES.getlist('images'):
                PostImage.objects.create(
                    post = post, #이게 있어야 어디에 연결되는지 알 수 있다.
                    photo = image_file,
                )

            #해시태그 입력
            tag_string = request.POST.get('tags')
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
                for tag_name in tag_names:
                    #태그를 있으면 가져오고 없으면 생성하라
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            url_next = reverse('posts:feeds') + f'#post-{post.id}'
            return HttpResponseRedirect(url_next)
            # return HttpResponseRedirect(f'/posts/feeds/#post-{post.id}')
    
    #포스트가 아닌 경우, form이 unvalid 해서 빠져나왔을 경우
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/post_add.html', context)

#해시태그
def tags(request, tag_name):
    try:
        #해시태그 네임을 받아옴
        tag = HashTag.objects.get(name=tag_name)
    #해시태그 정보가 없다면 아무것도 없는 posts를
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    #받아온 태그네임으로 게시글들을 필터링
    else:
        posts = Post.objects.filter(tags=tag)

    #필터링해서 해당하는걸 context에 전달
    context = {
        'tag_name': tag_name,
        'posts': posts
    }

    return render(request, 'posts/tags.html', context)
