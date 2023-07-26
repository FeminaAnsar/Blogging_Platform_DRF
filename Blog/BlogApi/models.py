from django.db import models
from AdminApi.models import User


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title


class ImageModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE,related_name='imagemodel_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    created_at = models.DateField(auto_now_add=True)


class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.comment

# Create your models here.
