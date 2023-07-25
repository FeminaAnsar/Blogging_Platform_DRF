from django.urls import path
from .views import (
            RegisterUserView,CreatePostView, DetailPostView, UpdatePostView, DeletePostView, AllPostListView,
            ImageView,PostCommentListView,CreateCommentView, CommentEditView,CommentDeleteView
    )


urlpatterns = [
    path('register/user/', RegisterUserView.as_view(),name='register-user'),

    path('post/create/', CreatePostView.as_view(),name='create-post'),
    path('post/<int:pk>/', DetailPostView.as_view(),name='post-detail'),
    path('post/update/<int:pk>/', UpdatePostView.as_view(),name='post-update'),
    path('post/delete/<int:pk>/', DeletePostView.as_view(),name='delete-post'),
    path('post/list/', AllPostListView.as_view(),name='post-list'),
    path('post/add-image/', ImageView.as_view(), name='image-post'),

    path('post/<int:pk>/comment/', CreateCommentView.as_view(),name='create-comment'),
    path('post/<int:pk>/comment-list/', PostCommentListView.as_view(),name='comment-list'),
    path('post/comment/edit/<int:pk>/', CommentEditView.as_view(),name='edit-comment'),
    path('post/comment/delete/<int:pk>/', CommentDeleteView.as_view(),name='delete-comment'),



]
