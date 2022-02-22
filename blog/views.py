import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from blog.forms import ArticlePostForm
from blog.models import ArticlePost, ArticleColumn
from comment.forms import CommentForm
from comment.models import Comment
from userprofile.models import Profile


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


def index(request):
    articles_popular = ArticlePost.objects.all().order_by('-total_views')

    search = request.GET.get('search')
    order_by = request.GET.get('order_by')

    if search:
        if order_by == 'total_views':
            articles = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
            order_by = 'total_views'
        else:
            articles = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-created_time')
            order_by = 'created_time'
    else:
        search = ''
        if order_by == 'total_views':
            articles = ArticlePost.objects.all().order_by('total_views')
            order_by = 'total_views'
        else:
            articles = ArticlePost.objects.all().order_by('-created_time')
            order_by = '-created_time'

    # 每页显示5篇文章
    paginator = Paginator(articles, 5)

    # 获取URL中的页码
    page = request.GET.get('page')

    # 将导航对讲相应的页码返回给articles
    articles = paginator.get_page(page)

    context = {"articles": articles, "articles_popular": articles_popular, 'order_by': order_by, 'search': search}
    return render(request, "blog/index.html", context=context)


def detail(request, id):
    article = ArticlePost.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body)

    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    comment_form = CommentForm()
    context = {"article": article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form}
    return render(request, "blog/detail.html", context=context)


@login_required
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST, request.FILES)

        if article_post_form.is_valid():
            # 保存数据，但但是不提交数据库
            new_article = article_post_form.save(commit=False)
            new_article.author = get(id=request.user.id)
            # 将新文章保存到数据库
            new_article.save()
            if request.POST['column'] != 'None':
                columns = request.POST.getlist("column")
                for c in columns:
                    column = ArticleColumn.objects.get(id=c)
                    new_article.column.add(column)
                    new_article.save()
            return redirect("blog:index")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {"article_post_form": article_post_form, 'columns': columns}
        return render(request, 'blog/create.html', context=context)


@login_required
def article_edit(request, id):
    if request.method == 'POST':
        pass
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {"article_post_form": article_post_form, "columns": columns}
        return render(request, "blog/edit.html", context=context)


# def article_most_popular(request):
#     articles_popular = ArticlePost.objects.all().order_by('-total_views')[:5]
#     context = {"articles_popular": articles_popular}
#     return render(request, "blog/right.html", context=context)


@login_required
def article_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("blog:index")
    else:
        return HttpResponse("仅允许post请求")


@login_required
def article_update(request, id):
    """
    更新文章的视图函数
    """
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            if request.POST['column'] != 'None':
                columns = request.POST.getlist("column")
                for c in ArticleColumn.objects.all():
                    if str(c.id) not in columns:
                        article.column.remove(c)
                        article.save()
                    else:
                        article.column.add(c)
                        article.save()

            return redirect("blog:detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {"article_post_form": article_post_form, "article": article, "columns": columns}
        return render(request, "blog/update.html", context=context)


def about(request):
    return render(request, "blog/about.html")