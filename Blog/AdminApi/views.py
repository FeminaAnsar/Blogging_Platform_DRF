from rest_framework import generics,status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth import logout
from rest_framework.response import Response
from .models import User
from BlogApi.models import PostModel,CommentModel
from .serializers import (
        RegisterNewAdminSerializer,AdminCommentSerializer,
        AdminPostCommentListSerializer,AdminPostSerializer
                          )
from BlogApi.pagination import CustomPagination


class RegisterNewAdminView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = RegisterNewAdminSerializer


class AdminPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer
    pagination_class = CustomPagination


class AdminPostDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer


class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer

    def delete(self, request, *args, **kwargs):
        return Response({'message': 'Post Deleted'})


class AdminPostCommentListView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostCommentListSerializer
    pagination_class = CustomPagination


class AdminDeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = CommentModel.objects.all()
    serializer_class = AdminCommentSerializer

    def delete(self, request, *args, **kwargs):
        return Response({'message': 'Comment Deleted'})


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response({'message':'Logout Successful'},status=status.HTTP_200_OK)

# Create your views here.
