from django.contrib import admin
from django.urls import path
from user.api import register, send_otp, verify_otp, login
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', login, name='login')
]

