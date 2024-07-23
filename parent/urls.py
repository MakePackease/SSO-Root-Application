from django.urls import path, include

from . import views
from parent.views import HomePageView, get_logged_in_users, register,login_, logout_view, login_as_user
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path('get_logged_in_users/', get_logged_in_users, name='get_logged_in_users'),
    path('logged_in_users_popup/', TemplateView.as_view(template_name='logged_in_users_popup.html'), name='logged_in_users_popup'),
    path("login/", views.login_, name="login_"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register_view"),
    path("home", HomePageView.as_view(), name="home"),
    path('login_as_user/<str:username>/', login_as_user, name='login_as_user'),
]
