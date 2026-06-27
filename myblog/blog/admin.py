from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["title", "content"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "post", "author", "created_at"]
    list_filter = ["created_at"]
