import os
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chovend.errors import UserError
from user.classes import UserClass
from product.classes import LocationClass, ProductClass
from product.serializers import ProductSerializer, ProductResponseSerializer, ProductUpdateSerializer, UpdateSocialMediaSerializer, UpdateSocialMediaResponseSerializer
from chovend.serializers import ErrorResponseSerializer, SuccessResponseSerializer
from chovend.utils import verify_user_in_token, verify_owner_of_product
from chovend.response import error_response, success_response
import requests


@api_view(['POST'])
def create_location_db(request):
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'cities.json')

    with open(file_path, 'r') as file:
        data = json.loads(file.read())

        print(type(data))
        location_obj = LocationClass()
        create_location_db = location_obj.create_location_db(data)

    return Response('Location DB Created!', status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        try:
            verify_user = verify_user_in_token(
                request, request.data['user'])
            
            product_data = serializer.data

            # Get user from DB to store against created product
            user_obj = UserClass()
            user = user_obj.get_user_by_id(product_data['user'])
            product_data['user'] = user

            location = LocationClass()
            location_city = location.get_city(city_id=product_data['location'])
            product_data['location'] = location_city


            product_obj = ProductClass() # Product Object

            # Check for duplicate product using title and description
            check_duplicate = product_obj.check_for_duplicate(title=product_data['title'], description=product_data['description'])

            # Create Product
            product = product_obj.create_product(product_data)

            serialized_product = ProductResponseSerializer(instance=product)

            return success_response(
                    input_=serialized_product.data, 
                    status_=status.HTTP_201_CREATED
                )

        except Exception as e:
            error_serializer = ErrorResponseSerializer(data={'message': str(e)})

            if error_serializer.is_valid():
                return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return error_response(
            input_=serializer,
            status_=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    try:
        verify_user = verify_user_in_token(request, request.data['user'])

        product_obj = ProductClass()
        product = product_obj.get_product_by_id(id=product_id)

        # Verify ownership of product
        verify_owner = verify_owner_of_product(request, product.user.id)

        serializer = ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return success_response(
                    input_=serializer.data, 
                    status_=status.HTTP_201_CREATED,
                    msg_='Product Updated!'
                )
        else:
            return error_response(
                    input_=serializer,
                    status_=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    msg_=str(serializer.error_messages)
                )

    except Exception as e:
        error_serializer = ErrorResponseSerializer(data={'message': str(e)})

        if error_serializer.is_valid():
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product_social_media(request, product_id):
    try:
        verify_user = verify_user_in_token(request, request.data['user'])
        serializer = UpdateSocialMediaSerializer(data=request.data)

        if serializer.is_valid():
            product_obj = ProductClass()
            product = product_obj.get_product_by_id(id=product_id)

            # Verify ownership of product
            verify_owner = verify_owner_of_product(request, product.user.id)

            update_product = product_obj.update_product_social_media(social_media_urls=serializer.data['social_media_urls'], product=product)

            serialize = UpdateSocialMediaResponseSerializer(instance=update_product)

            return success_response(
                    input_=serialize.data, 
                    status_=status.HTTP_201_CREATED,
                    msg_='Product Updated!'
                )
            
        else:
            return error_response(
                    input_=serializer,
                    status_=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    msg_=str(serializer.error_messages)
                )
    
    except Exception as e:
        error_serializer = ErrorResponseSerializer(data={'message': str(e)})

        if error_serializer.is_valid():
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        verify_user = verify_user_in_token(request, request.data['user'])

        product_obj = ProductClass()
        product = product_obj.get_product_by_id(id=product_id)

        # Verify ownership of product
        verify_owner = verify_owner_of_product(request, product.user.id)

        delete_product = product_obj.delete_product(product=product)

        return success_response(
                    input_={}, 
                    status_=status.HTTP_204_NO_CONTENT,
                    msg_='Product Deleted!'
                )
    
    except UserError as e:
        error_serializer = ErrorResponseSerializer(data={'message': str(e)})

        if error_serializer.is_valid():
            return Response(error_serializer.data, status=e.status)
        else:
            return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        error_serializer = ErrorResponseSerializer(data={'message': str(e)})

        if error_serializer.is_valid():
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)