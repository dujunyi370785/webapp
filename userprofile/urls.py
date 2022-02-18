from django.conf.urls.static import static
from django.urls import path
from userprofile import views
from webapp import settings

app_name = "userprofile"

urlpatterns = [
    path("login/", views.profile_login, name='login'),
    path("register/", views.profile_register, name="register"),
    path("edit/<int:id>/", views.profile_edit, name="edit"),
    path("logout/", views.profile_logout, name="logout"),
]

