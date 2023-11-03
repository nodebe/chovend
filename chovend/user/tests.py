from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.models import Otp


User = get_user_model()
client = APIClient()


user_data = {
            'email': 'testuser@gmail.com',
            'password': 'Password1#',
            'fullname': 'Test Register',
            'ip_address': '127.0.0.1'
        }

# Test for Register Endpoint
class TestAuthAPI(APITestCase):
    def setUp(self):
        self.data = {
            'email': 'testemail@gmail.com',
            'password': 'Password1#',
            'fullname': 'Test Register',
            'ip_address': '127.0.0.1'
        }
        self.user = User.objects.create(**self.data)
        self.user.set_password('Password1#')
        self.otp = Otp.objects.create(user=self.user, otp_value=12345)
    

    def test_register_success(self):
        url = reverse('register')

        response = client.post(url, data=user_data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['email'], 'testuser@gmail.com')

        # Check that the user was created in the database
        self.user = User.objects.get(email=response.data['data']['email'])
        self.user_id = self.user.id
        self.assertEqual(self.user.email, 'testuser@gmail.com')
    

    def test_register_insecure_password(self):
        url = reverse('register')

        insecure_password_data = user_data.copy()
        insecure_password_data['password'] = 'Pass1'

        response = client.post(url, data=insecure_password_data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'An error has occured!')
    
    def test_register_existing_email(self):
        url = reverse('register')

        response = client.post(url, self.data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'An error has occured!')
    

    def test_send_otp_success(self):
        send_otp_url = reverse('send_otp')

        # Get user
        user = User.objects.first()

        data = {
            'id': user.id
        }

        response = client.post(send_otp_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "OTP sent to email!")
        
        # Check that OTP was created
        self.assertEqual(Otp.objects.all().count(), 1)
    

    def test_send_otp_id_not_found(self):
        send_otp_url = reverse('send_otp')

        data = {
            'id': '7a31dd603feb4fde8e5c1cf12cf2c338'
        }

        response = client.post(send_otp_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "User matching query does not exist.")
    
    def test_send_otp_invalid_id(self):
        send_otp_url = reverse('send_otp')

        data = {
            'id': 'e596aba8c1d149759119a1978bd0b1f'
        }

        response = client.post(send_otp_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], "An error has occured!")
    
    
    def test_verify_otp_success(self):
        verify_otp_url = reverse('verify_otp')

        # Get OTP value
        otp = Otp.objects.first()
        otp_value = otp.otp_value

        data = {
            'id': self.user.id,
            'otp_value': 12345
        }

        response = client.post(verify_otp_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Verified!')


    def test_verify_otp_wrong_otp(self):
        verify_otp_url = reverse('verify_otp')
        
        # Get OTP value
        otp = Otp.objects.first()
        otp_value = otp.otp_value

        data = {
            'id': self.user.id,
            'otp_value': 12346
        }

        response = client.post(verify_otp_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Wrong OTP!')
    
    def test_login_incorrect_password(self):
        login_url = reverse('login')

        data = {
            'email': 'testemail@gmail.com',
            'password': 'Password1#'
        }

        response = client.post(login_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Incorrect Password!')
    
    def test_login_email_not_found(self):
        login_url = reverse('login')

        data = {
            'email': 'testemail1@gmail.com',
            'password': 'Password1#'
        }

        response = client.post(login_url, data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Email does not exist!')