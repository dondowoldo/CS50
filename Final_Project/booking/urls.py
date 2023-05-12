from django.urls import path
from . import views


app_name = "booking"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register")
]