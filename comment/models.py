from django.db import models
from django.contrib.auth.models import User
from blog.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_time',)

    def __str__(self):
        return self.body[:20]