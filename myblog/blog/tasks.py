from celery import shared_task
from django.core.cache import cache
from .models import Post


@shared_task
def clear_post_cache():
    """清除文章列表缓存（发布新文章或新评论时调用）"""
    cache.delete("posts_list")
    cache.delete_pattern("post_detail_*")
    return "cache cleared"


@shared_task
def send_comment_notification(comment_id):
    """模拟发送新评论通知（实际项目这里会发邮件）"""
    from .models import Comment
    comment = Comment.objects.get(id=comment_id)
    print(f"[Celery] 发送通知：{comment.author} 评论了文章「{comment.post.title}」")
    return f"notified author of comment {comment_id}"
