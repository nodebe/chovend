from django.contrib import admin
from django.urls import path
from user.api import register, send_otp, verify_otp
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Use email instead of username in the request data
        request.data['username'] = request.data['email']
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('send_otp/', send_otp),
    path('verify_otp/', verify_otp),
    path('login/', CustomTokenObtainPairView.as_view())
]

