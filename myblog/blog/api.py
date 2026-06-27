from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf(request):
    return Response({"csrf": get_token(request)})


@api_view(["GET"])
@permission_classes([AllowAny])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    content = request.data.get("content", "").strip()
    if content:
        comment = Comment.objects.create(post=post, author=request.user, content=content)
        return Response(CommentSerializer(comment).data, status=201)
    return Response({"error": "内容不能为空"}, status=400)


@api_view(["DELETE"])
def delete_comment(request, comment_id):
    if not request.user.has_perm("blog.delete_comment"):
        return Response({"error": "没有权限"}, status=403)
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return Response(status=204)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"username": user.username, "is_staff": user.is_staff})
    return Response({"error": "用户名或密码错误"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    if not username or not password:
        return Response({"error": "用户名和密码不能为空"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "用户名已存在"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return Response({"username": user.username}, status=201)


@api_view(["POST"])
def logout_api(request):
    logout(request)
    return Response({"ok": True})


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def current_user(request):
    if request.user.is_authenticated:
        return Response({
            "username": request.user.username,
            "is_staff": request.user.is_staff,
        })
    return Response(None)
