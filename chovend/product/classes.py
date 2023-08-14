from chovend.errors import UserError
from product.models import Country, State, City, Product, SocialMedia, ProductSocialMedia


class LocationClass:

    def get_city(self, city_id):
        city = City.objects.get(id=city_id)

        return city

    def get_or_create_country(self, country_name):
        country = Country.objects.get_or_create(country_name=country_name)

        return country[0]

    def get_or_create_state(self, state_name, country_name):
        state = State.objects.get_or_create(
            state_name=state_name, country=self.get_or_create_country(country_name=country_name))

        return state[0]

    def get_or_create_city(self, city_name, state_name, country_name):
        city = City.objects.get_or_create(
            city_name=city_name, state=self.get_or_create_state(state_name, country_name))

        return city[0]

    def create_location_db(self, data):
        for city_detail in data:
            city = city_detail['name']
            state = city_detail['state_name']
            country = city_detail['country_name']

            created = self.get_or_create_city(
                city_name=city, state_name=state, country_name=country)

            print(f'{created.id}. {city}==>{state}==>{country}')

        return True


class ProductClass:

    def get_product_by_id(self, id):
        product = Product.objects.get(id=id)

        return product

    def create_product(self, product_data):
        social_media_urls = product_data.pop('social_media_urls')

        product = Product.objects.create(**product_data)
        social_media = self.create_product_social_media(social_media_urls, product)

        return product

    def create_product_social_media(self, social_media_urls, product):
        for entry in social_media_urls:
            social_media_instance = SocialMedia.objects.get(id=entry["id"])
            ProductSocialMedia.objects.create(
                social_media=social_media_instance,
                product=product,
                url=entry["url"]
            )

        return True

    def check_for_duplicate(self, title, description):
        product = Product.objects.filter(title=title, description=description)

        if product:
            raise UserError('Product already exists with Title and Description!')
