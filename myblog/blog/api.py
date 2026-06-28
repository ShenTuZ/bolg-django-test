from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .tasks import clear_post_cache, send_comment_notification


@api_view(["GET"])
@permission_classes([AllowAny])
def post_list(request):
    """带 Redis 缓存的文章列表"""
    data = cache.get("posts_list")
    if data is not None:
        return Response(data)

    posts = Post.objects.all()
    serializer = PostListSerializer(posts, many=True)
    data = serializer.data
    cache.set("posts_list", data, 300)
    return Response(data)


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
        clear_post_cache.delay()
        send_comment_notification.delay(comment.id)
        return Response(CommentSerializer(comment).data, status=201)
    return Response({"error": "内容不能为空"}, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    if not request.user.has_perm("blog.delete_comment"):
        return Response({"error": "没有权限"}, status=403)
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return Response(status=204)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    """登录并返回 JWT token"""
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)
    if user is not None:
        token = AccessToken.for_user(user)
        return Response({
            "access": str(token),
            "username": user.username,
            "is_staff": user.is_staff,
        })
    return Response({"error": "用户名或密码错误"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    """注册并返回 JWT token"""
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    if not username or not password:
        return Response({"error": "用户名和密码不能为空"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "用户名已存在"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token = AccessToken.for_user(user)
    return Response({
        "access": str(token),
        "username": user.username,
        "is_staff": user.is_staff,
    }, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """从 JWT token 中获取用户信息"""
    return Response({
        "username": request.user.username,
        "is_staff": request.user.is_staff,
    })
