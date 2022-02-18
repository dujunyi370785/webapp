from django.contrib import admin

# Register your models here.
from blog import models

admin.site.register(models.ArticlePost)
admin.site.register(models.ArticleColumn)