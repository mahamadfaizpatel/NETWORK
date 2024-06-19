
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create/", views.create_post, name='create_post'),
    path("like/<int:post_id>", views.like, name='like'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('edit/<int:post_id>', views.edit, name='edit'),
    path('following/', views.following, name='following')
]
