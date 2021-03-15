from .models import Tag, Category, Product, Ingredient, Recipe
from django.forms import inlineformset_factory

IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=['type', 'quantity', 'unit'])


