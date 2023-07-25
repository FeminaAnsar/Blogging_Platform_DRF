from django.urls import path
from AdminApi.views import (
    RegisterNewAdminView, AdminPostListView, AdminPostDetailView, AdminPostDeleteView,
    AdminPostCommentListView, AdminDeleteCommentView,UserLogoutView
        )


urlpatterns = [
    path('register/admin/', RegisterNewAdminView.as_view(),name='register-admin'),

    path('post/list/', AdminPostListView.as_view(),name='post-list'),
    path('post/<int:pk>/', AdminPostDetailView.as_view(),name='post-detail'),
    path('post/delete/<int:pk>/', AdminPostDeleteView.as_view(),name='post-delete'),

    path('post/<int:pk>/comments/', AdminPostCommentListView.as_view(),name='post-comment-list'),
    path('comment/delete/<int:pk>/', AdminDeleteCommentView.as_view(),name='delete-comment'),

]
