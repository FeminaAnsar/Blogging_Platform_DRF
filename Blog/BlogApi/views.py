from .pagination import CustomPagination
from BlogApi.models import PostModel, ImageModel, CommentModel
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner
from AdminApi.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (  RegisterUserSerializer,ImageSerializer,
    CreateCommentSerializer,EditCommentSerializer, DeleteCommentSerializer, PostCommentListSerializer,
    CreatePostSerializer, DetailPostSerializer,UpdatePostSerializer,DeletePostSerializer,AllPostListSerializer
)


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message":  "Registration successful!!!Login credentials send to registered email"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = CreatePostSerializer

    def create(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == 0:
            serializer = CreatePostSerializer(data=self.request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(
                {'Error': 'Permission Denied..!', 'Message': 'Super user have no permission to create a post '})


class DetailPostView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = DetailPostSerializer


class UpdatePostView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,IsOwner]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = UpdatePostSerializer

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UpdatePostSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UpdatePostSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = DeletePostSerializer


class AllPostListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = AllPostListSerializer
    pagination_class = CustomPagination


class ImageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def create(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == 0:
            serializer = ImageSerializer(data=self.request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(
                {'Error': 'Permission Denied..!', 'Message': 'Super user have no permission to Add image to a post '})


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CommentModel.objects.all()
    serializer_class = CreateCommentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 0:
            serializer = CreateCommentSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(
                {'Error': 'Permission Denied..!', 'Message': 'Super user have no permission to comment a post '})


class PostCommentListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PostModel.objects.all()
    serializer_class = PostCommentListSerializer
    pagination_class = CustomPagination


class CommentEditView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]
    queryset = CommentModel.objects.all()
    serializer_class = EditCommentSerializer


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]
    queryset = CommentModel.objects.all()
    serializer_class = DeleteCommentSerializer


# Create your views here.
