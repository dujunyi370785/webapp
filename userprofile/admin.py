from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from userprofile.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# 定义一个行内admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'UserProfile'


# 将Profile 关联到User中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


# 重新注册User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
