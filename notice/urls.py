from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #
    path("list/", views.NoticeListView.as_view(), name='list'),
    path("update/", views.NoticeUpdateView.as_view(), name='update'),
]
