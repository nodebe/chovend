from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from chovend.response import error_response, success_response


@api_view(['POST'])
def register(request):
    user_ip_address = request.META.get('REMOTE_ADDR')
    print(user_ip_address)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = serializer.data

        response = success_response(input_=serializer.data, status_=status.HTTP_201_CREATED)

        return response

    else:
        response = error_response(input_ = serializer)

        return response

# @api_view(['POST'])