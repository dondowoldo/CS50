from django.contrib import admin
from .models import User, Listing, Comment, Message, Booking, PropertyType, AvailableDate

class UserAdmin(admin.ModelAdmin):
    list_display = "id", "username", "first_name", "last_name", "email","date_joined", "is_staff"

class ListingAdmin(admin.ModelAdmin):
    list_display = "id", "title", "creator", "price_per_night", "type", "date_created", "active"

class CommentAdmin(admin.ModelAdmin):
    list_display = "user", "listing", "comment", "timestamp"

class MessageAdmin(admin.ModelAdmin):
    list_display = "sent_from", "sent_to", "message", "timestamp"

class BookingAdmin(admin.ModelAdmin):
    list_display = "user", "listing", "total_price", "startdate", "enddate", "timestamp"

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = "type",

class AvailableDateAdmin(admin.ModelAdmin):
    list_display = "date",


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(AvailableDate, AvailableDateAdmin)
