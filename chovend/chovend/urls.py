from django.contrib import admin
from django.urls import path
from user.api import register, send_otp, verify_otp, login
from product.api import create_location_db, create_product, update_product, update_product_social_media, delete_product, get_product


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', login, name='login'),
    path('create_location_db', create_location_db, name='create_location_db'),
    path('product/create', create_product, name='create_product'),
    path('product/update/<str:product_id>/', update_product, name='update_product'),
    path('product/update/social_media/<str:product_id>/', update_product_social_media, name='update_product_social_media'),
    path('product/delete/<str:product_id>', delete_product, name='delete_product'),
    path('product/<str:product_id>/', get_product, name='get_product')
]

