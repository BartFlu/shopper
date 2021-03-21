from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Recipe, Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'  # name of elastic index
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product

        fields = [
            'id',
            'name',
        ]


@registry.register_document
class RecipeDocument(Document):
    class Index:
        name = 'recipes'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Recipe
        fields = [
            'id',
            'name',
        ]