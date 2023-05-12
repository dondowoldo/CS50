from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = "id", "username", "first_name", "last_name", "email","date_joined", "is_staff"

admin.site.register(User, UserAdmin)
