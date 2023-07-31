from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chovend.serializers import ErrorResponseSerializer
from chovend.utils import verify_user_in_token
from product.classes import LocationClass, ProductClass
from product.serializers import ProductSerializer
from user.classes import UserClass
import os, json


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
            verify_user = verify_user_in_token(request, request.data['user_id'])
            
            # Get user from DB to store against created product
            user_obj = UserClass()
            user = user_obj.get_user_by_id(serializer.data['user_id'])

            # Create Product
            product_obj = ProductClass()
            product_id = product_obj.create_product(user)

            # Add Product id to serializer data to be stored in Elastic Search
            serializer['product_id'] = product_id

        except Exception as e:
                error_serializer = ErrorResponseSerializer(data={'msg': str(e)})

                if error_serializer.is_valid():
                    return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(error_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    data = {
        'product': request.data,
    }

    return Response(data)