from django.core.mail import send_mail
from rest_framework import serializers,status
from AdminApi.models import User
from django.conf import settings
from BlogApi.models import PostModel, CommentModel, ImageModel
from django.template import Context
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.utils.html import strip_tags



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
            html_content = render_to_string('mail.html', {'title': 'Registration Email'})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives(subject,text_content,settings.DEFAULT_FROM_EMAIL,email_to)
            email.attach_alternative(html_content,'text/html')
            email.send()

            return user


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'content','created_at']
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
        fields = ['id', 'title', 'content','created_at','updated_at','images']


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'content','updated_at']
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
        fields = ['user', 'comment','created_at','updated_at']


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



