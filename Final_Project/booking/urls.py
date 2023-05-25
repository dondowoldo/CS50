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
    path("comments/<int:listing_id>", views.comments_view, name="comments"),
    path("my/properties", views.my_properties_view, name="my_properties"),
    path("my/properties/edit/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("my/properties/delete/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("my/bookings", views.my_bookings_view, name="my_bookings"),
    path("my/followed", views.my_followed_view, name="following")
]