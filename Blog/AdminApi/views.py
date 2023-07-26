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
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterNewAdminView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = RegisterNewAdminSerializer

    def post(self, request):
        serializer = RegisterNewAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "SuperUser(Admin) registration successful", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer
    pagination_class = CustomPagination


class AdminPostDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer


class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer


class AdminPostCommentListView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostCommentListSerializer
    pagination_class = CustomPagination


class AdminDeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = CommentModel.objects.all()
    serializer_class = AdminCommentSerializer


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        logout(request)
        return Response({'message':'Logout Successful'},status=status.HTTP_200_OK)

# Create your views here.
