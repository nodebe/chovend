from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import User
from .models import City, State, Country, SocialMedia, ProductStatus
from rest_framework_simplejwt.tokens import RefreshToken

client = APIClient()


product_data = {
    "user": '',
    "title": "Olabisi Wine Store",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc eleifend rhoncus nunc malesuada iaculis. Suspendisse non elit quis ipsum blandit accumsan id ac turpis. Donec tincidunt sem at sem finibus, congue posuere ante pellentesque. Morbi mattis libero eget sollicitudin volutpat. Nam ac condimentum magna. Mauris laoreet eros id sapien finibus dignissim. Aenean vulputate iaculis ipsum vitae varius. Donec vulputate fermentum vestibulum. Nam imperdiet ex at quam commodo fermentum. Ut elementum nulla vel nunc tincidunt elementum. Fusce non dui ac ante ornare condimentum. Quisque eros sapien, viverra sed fermentum non, tempor et massa. Etiam tellus ante, volutpat nec congue quis, laoreet eu lectus. Suspendisse potenti.",
    "location": "1",
    "social_media_urls": [
        {
            "id": 4,
            "url": "https://www.twitter.com/w_lete"
        },
        {
            "id": 5,
            "url": "https://wa.me/+2348108370073"
        }
    ],
    "website": "",
    "images": ["AFrHW1QRsWxmu5ZLU2qg"]
}


# for jwt auth
class TestCaseBase(APITestCase):

    @property
    def create_location(self):
        country = Country.objects.create(id=1, country_name='Nigeria')
        state = State.objects.create(id=1, state_name='Abuja Federal Capital Territory', country=country)
        city = City.objects.create(id=1, city_name='Bamburu', state=state)

    @property
    def create_social_media(self):
        facebook = SocialMedia.objects.create(id=1, social_media='Facebook')
        twitter = SocialMedia.objects.create(id=4, social_media='Twitter')
        whatsapp = SocialMedia.objects.create(id=5, social_media='Whatsapp')

    @property
    def create_product_status(self):
        active = ProductStatus.objects.create(id=1, status='Active')
        deleted = ProductStatus.objects.create(id=2, status='Deleted')
        suspended = ProductStatus.objects.create(id=3, status ='Suspended')
    
    @property
    def create_product(self):
        create_url = reverse('create_product')
        create = client.post(create_url, data=self.data, format='json', **self.token)
        created_product_id = create.data['data']['id']

        return created_product_id

    @property
    def bearer_token(self):
        "Create the bearer token for the endpoints that require it."
        user = User.objects.create_user(
            email='testuser@gmail.com', password='Password1#'
        )
        product_data['user'] = user.id

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
    

class TestProductAPI(TestCaseBase):
    "Tests for Products API - Create, Check for duplicate, edit, delete"
    def setUp(self):
        self.create_location
        self.create_social_media
        self.create_product_status
        self.token = self.bearer_token
        self.data = product_data

    def test_create_product(self):
        "Tests for creation of product"
        url = reverse('create_product')
        request = client.post(url, data=self.data, format='json', **self.token)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
    
    def test_create_existing_product(self):
        """Checks for existing product in DB using the title and description"""
        url = reverse('create_product')
        create = client.post(url, data=self.data, format='json', **self.token)

        duplicate = client.post(url, data=self.data, format='json', **self.token)

        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        "Tests for updating product"
        created_product_id = self.create_product

        update_url = reverse('update_product', kwargs={'product_id': created_product_id})

        self.data['title'] = 'Updated Title!'
        update = client.put(update_url, data=self.data, format='json', **self.token)

        self.assertEqual(update.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update.data['data']['title'], 'Updated Title!')

    def test_update_product_social_media(self):
        """Test for updating product social media"""

        created_product_id = self.create_product

        new_socials_data = {
            "user": self.data['user'],
            "social_media_urls": [
                {
                    "id": 4,
                    "url": "https://www.twitter.com/new_twitter"
                },
                {
                    "id": 5,
                    "url": "https://wa.me/+2348108370072"
                },
                {
                    "id": 1,
                    "url": "https://facebook.com/new_facebook"
                }
            ]
        }

        update_url = reverse('update_product_social_media', kwargs={'product_id': created_product_id})
        update = client.put(update_url, data=new_socials_data, format='json', **self.token)

        self.assertEqual(update.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update.data['message'], 'Product Updated!')
        self.assertEqual(update.data['data']['social_media_urls'][0]['url'], 'https://www.twitter.com/new_twitter')

    def test_delete_product(self):
        "Test for deleting product" 
        created_product_id = self.create_product

        delete_url = reverse('delete_product', kwargs={'product_id': created_product_id})
        data_user = {'user': self.data['user']}

        delete = client.delete(delete_url, data=data_user, format='json', **self.token)

        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(delete.data['message'], 'Product Deleted!')
    
    def test_get_single_product(self):
        "Get Individual product with id"
        created_product_id = self.create_product

        get_product_url = reverse('get_product', kwargs={'product_id': created_product_id})
        get_product = client.get(get_product_url, format='json')

        self.assertEqual(get_product.status_code, status.HTTP_200_OK)
        self.assertEqual(get_product.data['data']['id'], created_product_id)

    def test_get_social_media_list(self):
        "Test for getting list of social media"
        get_url = reverse('get_social_media_list')
        get_media = client.get(get_url, format='json', **self.token)

        self.assertEqual(get_media.status_code, status.HTTP_200_OK)
        self.assertEqual(get_media.data['data']['socials'][0]['social_media'], 'Facebook')
        self.assertEqual(get_media.data['data']['socials'][0]['id'], 1)