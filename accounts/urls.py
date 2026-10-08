from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),

    path("login/", views.login_view, name="login"),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin-dashboard/edit/<int:student_id>/",
        views.admin_edit_student,
        name="admin_edit_student"
    ),

    path(
        "admin-dashboard/delete/<int:student_id>/",
        views.admin_delete_student,
        name="admin_delete_student"
    ),
]