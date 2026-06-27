from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>/", views.detail, name="detail"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
