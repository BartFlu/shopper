from .models import Tag, Category, Product, Ingredient, Recipe
from django import forms


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['tags', 'name', 'source']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['type', 'quantity', 'unit']



