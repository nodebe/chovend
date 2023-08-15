from django.contrib import admin
from .models import Product, City, State, Country, SocialMedia, ProductSocialMedia

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id"
    )
    list_filter = [
        "user",
        "id"
    ]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city_name",
        "state",
        "get_country_name"
    )
    list_filter = [
        "state",
        "state__country"
    ]

    ordering = ["state__country__country_name", "state", "city_name"]

    def get_country_name(self, obj):
        # Custom method to get country_name from the associated Country model
        return obj.state.country.country_name

    get_country_name.short_description = "Country"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "state_name",
        "country"
    )
    list_filter = [
        "country"
    ]

    ordering = ["country", "state_name"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "country_name",
    )

    ordering = ["country_name"]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "social_media",
    )

    ordering = ["id"]


@admin.register(ProductSocialMedia)
class ProductSocialMediaAdmin(admin.ModelAdmin):
    list_display = (
        "social_media",
        "product",
        "url",
    )

    ordering = ["product"]
