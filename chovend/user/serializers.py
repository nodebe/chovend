from rest_framework import serializers
from user.models import User, Otp
from password_validator import PasswordValidator
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    ip_address = serializers.IPAddressField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        read_only_fields = ['id']
        fields = read_only_fields + [
            'email', 
            'fullname',
            'password',
            'ip_address'
        ]
    
    def validate_password(self, value):
        ''' Checks and verifies that password is secure
            Password must have minimum of 6 characters, have an uppercase, a lowercase, a number, and a symbol
        '''
        schema = PasswordValidator()
        schema.min(6).uppercase().lowercase().digits().symbols()

        if not schema.validate(value):
            raise serializers.ValidationError(
                'Password not secure! Must contain minimum of 6 characters, an uppercase, a lowercase, a number, and a symbol')
        
        hashed_password = make_password(value)
        return hashed_password

class UserIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex')

    
class OTPSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex')
    otp_value = serializers.IntegerField(write_only=True)