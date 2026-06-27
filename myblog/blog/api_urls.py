from django.urls import path
from . import api

urlpatterns = [
    path("csrf/", api.get_csrf, name="api_csrf"),
    path("posts/", api.post_list, name="api_post_list"),
    path("posts/<int:post_id>/", api.post_detail, name="api_post_detail"),
    path("posts/<int:post_id>/comments/", api.add_comment, name="api_add_comment"),
    path("comments/<int:comment_id>/delete/", api.delete_comment, name="api_delete_comment"),
    path("login/", api.login_api, name="api_login"),
    path("register/", api.register_api, name="api_register"),
    path("logout/", api.logout_api, name="api_logout"),
    path("me/", api.current_user, name="api_current_user"),
]
