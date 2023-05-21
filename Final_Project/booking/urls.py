from django.urls import path
from . import views


app_name = "booking"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.addProperty, name="add"),
    path("detail/<int:listing_id>",views.detail_view, name="detail"),
    path("book/<int:listing_id>", views.book_view, name="book"),
    path("comments/<int:listing_id>", views.comments_view, name="comments")
]