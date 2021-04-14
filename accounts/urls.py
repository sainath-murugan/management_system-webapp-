from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("user", views.user, name="user"),
    path("account_setting", views.account_setting, name="account_setting"),
    path("products", views.products, name="products"),
    path("login_user", views.login_user, name="login"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("register", views.register, name="register"),
    path("customers/<str:id>", views.customers, name="customer"),
    path("create_order/<str:id>", views.create_order, name="create_order"),
    path("update_order/<str:id>", views.update_order, name="update_order"),
    path("delete_order/<str:id>", views.delete_order, name="delete_order"),
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"), name="reset_password"),
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password_email.html"), name="password_reset_confirm"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]

