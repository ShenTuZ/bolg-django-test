from rest_framework import serializers
from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "author_name", "created_at"]


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", default="未分类", read_only=True)
    author_name = serializers.CharField(source="author.username", read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "category_name", "author_name", "created_at", "comment_count"]

    def get_comment_count(self, obj):
        return obj.comment_set.count()


class PostDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", default="未分类", read_only=True)
    author_name = serializers.CharField(source="author.username", read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "category_name", "author_name", "created_at", "comments"]

    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data
