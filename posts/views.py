from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
# render: 어떤 템플릿을 그릴 것인지

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def index(request):
    posts = Post.objects.all()
    context = { 'posts' : posts }
    return render(request, 'posts/index.html', context)

def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = { 'post' : post }
    return render(request, 'posts/detail.html', context)

@login_required
def new(request): 
    return render(request, 'posts/new.html')    

@login_required
def create(request):
#    if not request.user.is_authenticated:
#        return redirect('accounts:login') 
# login_required 기능을 사용하지 않는다면 위 두줄 코드를 사용해야 함.

    user = request.user
    body = request.POST['body']

    image = None
    if 'image' in request.FILES:
        image = request.FILES['image']

    post = Post(user=user, body=body, image=image, created_at=timezone.now())
    post.save()

    return redirect('posts:detail', post_id=post.id)    

@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')

    context = { 'post' : post }
    return render(request, 'posts/edit.html', context)   

@login_required
def update(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')

    post.body = request.POST['body']

    if 'image' in request.FILES:
        post.image = request.FILES['image']

    post.save()

    return redirect('posts:detail', post_id=post.id)        

@login_required
def delete(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')
    
    post.delete()

    return redirect('posts:index')   

@login_required
def like(request, post_id):

    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)

            if request.user in post.liked_users.all():
                post.liked_users.remove(request.user)
            else:
                post.liked_users.add(request.user)

            return redirect('posts:detail', post_id=post.id)

        except Post.DoesNotExist:
            pass

    return redirect('posts:index')