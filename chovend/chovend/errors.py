from rest_framework import status

class UserError(Exception):
    def __init__(self, message='An error occured', status=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status = status

    def __str__(self):
        return self.message

class ServerError(Exception):
    def __init__(self, message='Internal Server error!', status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status = status
    
    def __str__(self):
        return self.message