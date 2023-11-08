from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product


@registry.register_document
class ProductDocument(Document):
    "Product Document in ElasticSearch"
    class Index:
        "Setup the index of the elastic search"
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    location = fields.TextField(attr='location_indexing')
    location_keyword = fields.KeywordField(
        fields={'raw': fields.KeywordField()})

    class Django:
        """Create the model from postgresql in elastic search"""
        model = Product
        fields = [
            'title',
            'search_description',
        ]

        ignore_signals = False

    def prepare_location(self, instance):
        "Use the location_indexing method to prepare the location field for indexing"
        return instance.location_indexing()
