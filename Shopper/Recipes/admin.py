from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Tag, Category, Recipe, Ingredient, Product, ShoppingList, MyUser
# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(ShoppingList)
admin.site.register(MyUser, UserAdmin)

