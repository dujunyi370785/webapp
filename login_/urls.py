from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from login import views
from webapp import settings

app_name = "login"

urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path("index/", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name='register'),
    path("logout/", views.logout, name="logout"),
    path("confirm/", views.user_confirm, name="user_confirm"),
    path("user-edit/<int:id>/", views.edit_user, name="user_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
