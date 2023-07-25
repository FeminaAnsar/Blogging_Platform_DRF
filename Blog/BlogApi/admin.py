from django.contrib import admin
from BlogApi import models


@admin.register(models.PostModel)
class AdminPost(admin.ModelAdmin):
    fields = ['user','title','content']
    list_display = ['id','user_id','title','content','created_at','updated_at']


@admin.register(models.CommentModel)
class AdminComment(admin.ModelAdmin):
    fields = ['user','post','comment']
    list_display = ['id','comment','user_id','post_id','created_at','updated_at']


@admin.register(models.ImageModel)
class AdminImage(admin.ModelAdmin):
    fields = ['post', 'user', 'image']
    list_display = ['id','post_id', 'user_id', 'image', 'created_at']

# Register your models here.
