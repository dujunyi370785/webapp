# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost
from mdeditor.fields import MDTextFormField


# 文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 数据模型
        model = ArticlePost

        # 表单包含的字段
        fields = ('title', 'body', 'avatar')
