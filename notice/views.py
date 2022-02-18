from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from blog.models import ArticlePost


class NoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/userprofile/login'

    # 未读消息集合
    def get_queryset(self):
        return self.request.user.notifications.unread()


class NoticeUpdateView(View):
    """更新通知状态"""

    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')
