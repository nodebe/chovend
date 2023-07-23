from rest_framework.response import Response
from rest_framework import status
from chovend.serializers import ErrorResponseSerializer, SuccessResponseSerializer


def error_response(input_):
    response = ErrorResponseSerializer(
            data = {'data': input_.errors}
        )
    if response.is_valid():
        return Response(
            response.data, 
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            response.errors, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def success_response(input_, status_):
    response = SuccessResponseSerializer(
            data = {'data': input_}
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