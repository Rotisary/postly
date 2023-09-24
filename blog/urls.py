from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentListView,
    CommentCreateView,
    CommentDeleteView,
    LatestPostListView,
    PostLikesAPI
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('posts/latest/', LatestPostListView.as_view(), name='latest-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', views.post_likes, name='post_like'),
    path('api/post/<int:pk>/like/', PostLikesAPI.as_view(), name='post_like_api'),
    path('post/<int:pk>/comments/', CommentListView.as_view(), name='comments'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/drop-comment/', CommentCreateView.as_view(), name='drop-comment'),
    path('search/', views.Search, name='search'),
    path('trending/', views.trending, name='trending'),
    path('about/', views.about, name='blog-about')   
]