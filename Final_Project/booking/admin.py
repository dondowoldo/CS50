from django.contrib import admin
from .models import User, Listing, Comment, Message

class UserAdmin(admin.ModelAdmin):
    list_display = "id", "username", "first_name", "last_name", "email","date_joined", "is_staff"

class ListingAdmin(admin.ModelAdmin):
    list_display = "id", "name", "creator", "price_per_day", "property_type", "date_created", "active"

class CommentAdmin(admin.ModelAdmin):
    list_display = "user", "listing", "comment", "timestamp"

class MessageAdmin(admin.ModelAdmin):
    list_display = "sent_from", "sent_to", "message", "timestamp"

class BookingAdmin(admin.ModelAdmin):
    list_display = "user", "listing", "total_price", "duration", "timestamp"

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)