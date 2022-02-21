from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField


class ArticleColumn(models.Model):
    """博客分类"""
    # 栏目名称
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客栏目'
        verbose_name_plural = '博客栏目'
        ordering = ('-created_time',)


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = MDTextField()
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='articles/%Y%m%d/', blank=True)

    column = models.ManyToManyField(
        ArticleColumn,
        null=True,
        blank=True,
        related_name='article'
    )

    class Meta:
        ordering = ('-created_time',)
        verbose_name = "博客"
        verbose_name_plural = "博客"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.id])

    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article
