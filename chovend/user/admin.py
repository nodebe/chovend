from django.contrib import admin
from user.models import User, Otp

# Register your models here.
admin.site.register(Otp)

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
     