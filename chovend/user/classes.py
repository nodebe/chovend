import random
from user.models import Otp, User
from django.utils import timezone
from rest_framework import status
from chovend.senders import send_email
from chovend.errors import UserError
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserClass:

    def get_user_by_id(self, id:str):
        user = User.objects.filter(id=id).first()

        return user

    def get_user_by_email(self, email:str):
        user = User.objects.filter(email=email).first()

        return user
    
    def verify_login_password(self, db_password, login_password):
        if check_password(login_password, db_password):
            return True
        else:
            raise UserError('Incorrect Password!')

    def login_user(self, data:dict):
        user = self.get_user_by_email(data['email'])

        if user == None:
            raise UserError('Email does not exist!', '404')

        # Verify User's password
        self.verify_login_password(db_password=user.password, login_password=data['password'])

        # Update last login
        self.update_last_login(user)

        # Generate JWT Token for user.
        token = RefreshToken.for_user(user).access_token

        user_data = {
            **user.__dict__,
            'token': str(token)
        }

        return user_data

    def update_last_login(self, user):
        user.last_login = timezone.now()
        user.save()

class OTPClass:

    def get_otp_row(self, user):
        otp = Otp.objects.get(user=user.id)
        return otp

    def generate_otp(self, user):
        self.otp = str(random.randint(10000, 99999))
        self.store_otp(user)
        return self.otp
    
    def store_otp(self, user):
        '''Stores OTP linked with user model!'''
        set_otp = Otp(user=user, otp_value=self.otp, created_at=timezone.now())
        set_otp.status = False
        set_otp.save()
    
    def send_otp_to_email(self, email):
        subject = 'One-Time Password for Chovend'
        message = f"Your One Time Password is {self.otp}. It will expire in 5(five) minutes"

        send_email(subject=subject, recipient=email, message=message)
        return True

    def verify_otp(self, user, otp):
        '''Verify the otp of user if valid and correct'''
        if user.verified:
            raise UserError('User already verified!')
        
        self.check_otp_values(input_otp=otp, user_otp=user.otp.otp_value)
        self.check_time_validity(user.otp.created_at)

        user.verified = True
        user.is_active = True
        user.otp.save()
        user.save()

    
    def check_otp_values(self, input_otp, user_otp):
        if input_otp != user_otp:
            raise UserError('Wrong OTP!', status=status.HTTP_401_UNAUTHORIZED)
        
        return True
    
    def check_time_validity(self, otp_time_created):
        created_at = otp_time_created
        current_time = timezone.now()

        time_difference = current_time - created_at
        time_difference_minutes = time_difference.seconds / 60

        if time_difference_minutes > 5:
            raise UserError('OTP expired!', '401')
        
        return True