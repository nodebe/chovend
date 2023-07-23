from django.contrib import admin
from django.urls import path
from user.api import register, send_otp, verify_otp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('send_otp/', send_otp),
    path('verify_otp/', verify_otp)
]
