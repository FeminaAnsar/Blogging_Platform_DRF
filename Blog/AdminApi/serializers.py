from rest_framework import serializers
from .models import User
from BlogApi.models import PostModel, CommentModel
from rest_framework.response import Response
from BlogApi.serializers import CommentUserSerializer,ImageSerializer


class RegisterNewAdminSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=False,read_only=True)
    is_staff = serializers.BooleanField(default=False,read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_superuser', 'is_staff']
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'email': {'required': True},
                        'username': {'required': True},
                        'password': {'write_only': True, 'required': True}
                        }

    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data['username']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username Already taken.Please try another one")
        else:
            user = User.objects.create_superuser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user


class AdminPostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, source='imagemodel_set')
    user = CommentUserSerializer()
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'user','images','created_at','updated_at']


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        exclude = ['post']

    def to_representation(self, instance):
        represent = super(AdminCommentSerializer, self).to_representation(instance)
        represent['user'] = instance.user.username
        return represent


class AdminPostCommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content','created_at','updated_at','comments']

    def get_comments(self, obj):
        comments = CommentModel.objects.filter(post=obj)
        try:
            serializer = AdminCommentSerializer(comments, many=True)
        except Exception as e:
            return Response({"error":e})
        return serializer.data

