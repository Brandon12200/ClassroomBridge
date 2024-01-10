
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("classes/", views.classes, name="classes"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    path('check_login_status', views.check_login_status, name='check_login_status'),
]
