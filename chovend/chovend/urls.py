from django.contrib import admin
from django.urls import path
from user.api import register, send_otp, verify_otp, login
from product.api import create_location_db, create_product


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', login, name='login'),
    path('create_location_db', create_location_db, name='create_location_db'),
    path('create_product/', create_product, name='create_product')
]

