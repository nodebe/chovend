from rest_framework.response import Response
from rest_framework import status
from chovend.serializers import ErrorResponseSerializer, SuccessResponseSerializer


def error_response(input_, status_, msg_='An error has occured!'):
    response = ErrorResponseSerializer(
            data = {'data': input_.errors, 'message': msg_}
        )
    if response.is_valid():
        return Response(
            response.data, 
            status=status_
        )
    else:
        return Response(
            response.errors, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def success_response(input_, status_, msg_='Success!'):
    response = SuccessResponseSerializer(
            data = {'data': input_, 'message': msg_}
        )
    if response.is_valid():
        return Response(
            response.data, 
            status=status_
        )
    else:
        return Response(
            response.errors, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )