from django.contrib import admin
from . models import Tag, Category, Recipe, Ingredient, Product
# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(Recipe)

