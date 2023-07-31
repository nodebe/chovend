from rest_framework import serializers
from product.models import SocialMedia

class SocialMediaSerializer(serializers.ModelSerializer):
    url = serializers.URLField(allow_blank=True)
    class Meta:
        model = SocialMedia
        fieds = ['id', 'social_media']

class ProductSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(format='hex')
    title = serializers.CharField()
    description = serializers.CharField()
    location = serializers.CharField()
    social_medial_urls = SocialMediaSerializer(many=True)
    website = serializers.URLField(allow_blank=True)
    images = serializers.ListField(allow_empty=False, min_length=1, max_length=5)