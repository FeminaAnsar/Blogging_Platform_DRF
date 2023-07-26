from django.core.mail import send_mail
from rest_framework import serializers,status
from AdminApi.models import User
from django.conf import settings
from BlogApi.models import PostModel, CommentModel, ImageModel


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 'email': {'required': True},
                        'username': {'required': True}, 'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data['username']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken')
        else:
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()

            email_to = [user.email]
            subject = 'Registration mail'
            message = f"""
                Welcome to our Blogging Platform.Thank you for registering.\n
                First Name : {user.first_name}\n
                Last Name : {user.last_name}\n
                Email : {user.email}\n
                Username : {user.username}\n
                Password : {self._validated_data['password']}\n
                Please Login with above credentials

                """

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, email_to)

            return user


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'content']
        extra_kwargs = {'title': {'required': True}, 'content': {'required': True}}

    def create(self, validated_data):
        user = self.context.get('user')
        post = PostModel.objects.create(user=user, **validated_data)
        post.save()
        return post


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageModel
        fields = ['post', 'image']
        extra_kwargs = {'post': {'required': True}, 'image': {'required': True}}

    def create(self, validated_data):
        user=self.context.get('user')
        image = ImageModel.objects.create(user=user, **validated_data)
        image.save()
        return image


class DetailPostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, source='imagemodel_set')
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'updated_at','images']


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'content']
        extra_kwargs = {'title': {'required': True}, 'content': {'required': True}}


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'


class AllPostListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, source='imagemodel_set')
    user = CommentUserSerializer()
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'user','images']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['post', 'comment']
        extra_kwargs = {'post': {'required': True}, 'comment': {'required': True}}

    def create(self, validated_data):
        user = self.context.get('user')
        comment = CommentModel.objects.create(user=user, **validated_data)
        comment.save()
        return comment


class EditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment']


class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()

    class Meta:
        model = CommentModel
        fields = ['user', 'comment', 'updated_at']


class PostCommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    user = CommentUserSerializer()
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'comments','user']

    def get_comments(self, obj):
        comments = CommentModel.objects.filter(post=obj)
        try:
            serializer = CommentSerializer(comments, many=True)
        except Exception as e:
            print(e)
        return serializer.data



