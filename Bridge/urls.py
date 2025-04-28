
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register_view, name="register"),
    path("classes/", views.classes, name="classes"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("new_class/", views.new_class, name="new_class"),
    path("view_class/<int:class_id>/", views.view_class, name="view_class"),
    path("view_module/<int:module_id>/<int:class_id>/", views.view_module, name="view_module"),
    path("add_module/<int:class_id>/", views.add_module, name="add_module"),
    path("add_student/<int:class_id>/", views.add_student, name="add_student"),
    path("student_form/<int:class_id>/", views.student_form, name="student_form"),
    path("remove_student/<int:class_id>/<int:student_id>/", views.remove_student, name="remove_student"),
    path("edit_class_homepage/<int:class_id>/", views.edit_class_homepage, name="edit_class_homepage"),

    path('check_login_status', views.check_login_status, name='check_login_status'),
]
