from django.contrib import admin
from user.models import User, Otp

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "fullname",
        "ip_address"
    )
    list_filter = [
        "email"
    ]
     
@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "otp_value",
        "created_at"
    )
    list_filter = [
        "user"
    ]
     