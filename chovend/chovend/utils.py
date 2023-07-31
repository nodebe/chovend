from chovend.errors import UserError
from user.models import User
import os, jwt
from rest_framework import status

def verify_user_in_token(request, user_id):
    raw_token = request.auth
    validated_token = jwt.decode(str(raw_token), key=os.environ.get('SECRET_KEY'), algorithms=['HS256'])

    check_user_ids = (validated_token['user_id'] == user_id)

    check_user_is_admin = User.objects.get(id=user_id)
    if check_user_ids or check_user_is_admin.is_superuser:
        return True
    else:
        raise UserError(message='Unauthorised User!', status=status.HTTP_401_UNAUTHORIZED)


