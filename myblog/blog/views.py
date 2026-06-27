from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Post, Comment


def index(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html", {"posts": posts})


def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all()
    return render(request, "blog/detail.html", {"post": post, "comments": comments})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if username and password and not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("index")
    return render(request, "blog/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "index")
            return redirect(next_url)
    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@permission_required("blog.delete_comment", raise_exception=True)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect("detail", post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    if content:
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect("detail", post_id=post_id)
