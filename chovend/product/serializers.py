"Serializers for Product parameters"
from rest_framework import serializers
from product.models import SocialMedia, City, State, Country, Product, ProductSocialMedia


class SocialMediaInputSerializer(serializers.ModelSerializer):
    "Social Media serializer"
    id = serializers.CharField()
    url = serializers.URLField(allow_blank=True)

    class Meta:
        "Meta info associated with SocialMedia models"
        model = SocialMedia
        fields = ['id', 'url']

class SocialMediaSerializer(serializers.ModelSerializer):
    "Social Media serializer"

    class Meta:
        "Meta info associated with SocialMedia models"
        model = SocialMedia
        fields = ['id', 'social_media']

class SocialMediaResponseSerializer(serializers.Serializer):
    data = SocialMediaSerializer(many=True)


class ProductSocialMediaSerializer(serializers.ModelSerializer):
    "Product Social Media serializer"
    url = serializers.URLField(allow_blank=True)
    social_media = SocialMediaSerializer()

    class Meta:
        "Meta info associated with SocialMedia models"
        model = ProductSocialMedia
        fields = ['url', 'social_media']


class ProductSocialMediaField(serializers.BaseSerializer):
    """
    Custom serializer field to handle the many-to-many relationship
    between Product and SocialMedia through ProductSocialMedia.
    """
    def to_representation(self, obj):
        # obj is the Product instance
        product_social_media = ProductSocialMedia.objects.filter(product=obj.instance)
        serialized_data = ProductSocialMediaSerializer(product_social_media, many=True).data

        return serialized_data
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        "Meta info associated with Country models"
        model = Country
        fields = ['id', 'country_name']

class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        "Meta info associated with SocialMedia models"
        model = State
        fields = ['id', 'state_name', 'country']

class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        "Meta info associated with SocialMedia models"
        model = City
        fields = ['id', 'city_name', 'state']


class ProductSerializer(serializers.Serializer):
    "Product Serializer"
    user = serializers.UUIDField(format='hex')
    title = serializers.CharField()
    description = serializers.CharField()
    location = serializers.CharField()
    social_media_urls = SocialMediaInputSerializer(many=True)
    website = serializers.URLField(allow_blank=True)
    images = serializers.ListField(
        allow_empty=False, min_length=1, max_length=5)

class ProductUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    fullname = serializers.CharField()

class ProductUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        allow_empty=False, min_length=1, max_length=5)
    
    class Meta:
        model = Product
        read_only_fields = ['id']
        fields = read_only_fields + ['title', 'description', 'location', 'website', 'images']


class ProductResponseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = ProductUserSerializer()
    location = CitySerializer()
    social_media_urls = ProductSocialMediaField()
    images = serializers.ListField(
        allow_empty=False, min_length=1, max_length=5)

    class Meta:
        "Meta info associated with Product models"
        model = Product
        fields = ['id', 'user', 'title', 'description', 'location', 'social_media_urls', 'website', 'images']
    
class UpdateSocialMediaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.UUIDField(format='hex')
    social_media_urls = SocialMediaInputSerializer(many=True)

class UpdateSocialMediaResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    social_media_urls = ProductSocialMediaField()