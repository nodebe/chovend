from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chovend.serializers import ErrorResponseSerializer
from user.classes import OTPClass, UserClass
from user.models import User
from user.serializers import UserSerializer, UserIDSerializer, OTPSerializer, UserLoginSerializer, UserLoginResponseSerializer
from chovend.response import error_response, success_response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    user_ip_address = request.META.get('REMOTE_ADDR')
    print(user_ip_address)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return success_response(
            input_=serializer.data, 
            status_=status.HTTP_201_CREATED
        )

    else:
        return error_response(
            input_=serializer,
            status_=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def send_otp(request):
    serializer = UserIDSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(id=serializer.data['id'])
            
            otp_object = OTPClass()
            otp_object.generate_otp(user)
            otp_object.send_otp_to_email(user.email)

            return success_response(
                input_=serializer.data, 
                status_=status.HTTP_201_CREATED,
                msg_='OTP sent to email!'
            )
        
        except Exception as e:
            error_serializer = ErrorResponseSerializer(data={'msg': str(e)})

            if error_serializer.is_valid():
                return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return error_response(
            input_=serializer
        )

@api_view(['POST'])
def verify_otp(request):
    serializer = OTPSerializer(data = request.data)

    if serializer.is_valid():
        try:
            user = User.objects.get(id=serializer.data['id'])
            
            otp_object = OTPClass()
            otp_object.verify_otp(user, request.data['otp_value'])
            
            return success_response(
                input_=serializer.data, 
                status_=status.HTTP_201_CREATED,
                msg_='Verified!'
            )
        
        except Exception as e:
            error_serializer = ErrorResponseSerializer(data={'msg': str(e), 'data':{'id': serializer.data['id']}})

            if error_serializer.is_valid():
                return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(serializer.errors)
    
@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data = request.data)

    if serializer.is_valid():
        try:
            user_object = UserClass()
            login_user = user_object.login_user(serializer.data)
            print(login_user)
            response_serializer = UserLoginResponseSerializer(data=login_user)
            
            if response_serializer.is_valid():
                return Response(response_serializer.data)
            else:
                return Response(response_serializer.errors)
                return error_response(
                    input_=serializer,
                    status_=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    msg_=str(response_serializer.error_messages)
                )
        
        except Exception as e:
            error_serializer = ErrorResponseSerializer(data={'msg': str(e)})

            if error_serializer.is_valid():
                return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    else:
        return Response(serializer.errors)