from django.urls import path
from rest_framework_simplejwt.views import token_refresh
from . import api

urlpatterns = [
    path("posts/", api.post_list, name="api_post_list"),
    path("posts/<int:post_id>/", api.post_detail, name="api_post_detail"),
    path("posts/<int:post_id>/comments/", api.add_comment, name="api_add_comment"),
    path("comments/<int:comment_id>/delete/", api.delete_comment, name="api_delete_comment"),
    path("login/", api.login_api, name="api_login"),
    path("register/", api.register_api, name="api_register"),
    path("me/", api.current_user, name="api_current_user"),
    path("token/refresh/", token_refresh, name="api_token_refresh"),
]
