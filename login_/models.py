import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    user_name = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    cellphone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    create_time = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length=500, blank=True)

    update_time = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Profile(models.Model):
    user = models.OneToOneField(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y/%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return "user {}".format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user_name + ":   " + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
