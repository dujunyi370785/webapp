from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blog.models import ArticlePost
from comment.forms import CommentForm
from comment.models import Comment


def check_login(fn):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_login', False):
            return fn(request, *args, **kwargs)
        else:
            # 获得用户当前访问的url，并传递给/user/login/
            next = request.get_full_path()
            print(next)
            red = HttpResponseRedirect('/login/login/?next=' + next)
            return red

    return wrapper


@login_required
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
