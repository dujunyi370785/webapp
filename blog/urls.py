from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("detail/<int:id>/", views.detail, name="detail"),
    path("article-create/", views.article_create, name="article_create"),
    path("article-delete/<int:id>/", views.article_delete, name="article_delete"),
    path("article-update/<int:id>/", views.article_update, name="article_update"),
    path("about/", views.about, name="about"),
]