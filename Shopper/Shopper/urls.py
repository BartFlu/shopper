"""Shopper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Recipes import view_auth
from Recipes.views import basket, main_view, models_manipulation, shopping_list


urlpatterns = [
    path('', main_view.MainView.as_view(), name='main'),
    path('filtered/<tag>', main_view.MainViewFiltered.as_view(), name='main_filtered'),
    path('advancedFilter/', main_view.advanced_filter_view, name='advanced_filter'),

    path('addToBasket/<int:pk>', basket.add_to_basket, name='addToBasket'),
    path('removeFromBasket/<int:pk>', basket.remove_from_basket, name='removeFromBasket'),
    path('basket', basket.BasketView.as_view(), name='basket'),
    path('toShoppinglist', basket.convert_to_shopping_list, name='convert'),

    path('shoppingList', shopping_list.ShoppingListView.as_view(), name='shoppingList'),
    path('sendList', shopping_list.send_list, name='sendList'),
    path('addComment/<int:pk>', shopping_list.add_comment_to_shopping_item, name='add_comment'),
    path('deleteShoppingItem/<int:pk>', shopping_list.remove_from_shopping_list, name='removeFromList'),

    path('recipe/<int:pk>', models_manipulation.RecipeDetails.as_view(), name='recipe'),
    path('updateRecipe/<int:pk>', models_manipulation.UpdateRecipe.as_view(), name='edit_recipe'),
    path('addRecipe', models_manipulation.AddRecipe.as_view(), name='add_recipe'),
    path('removeRecipe/<int:pk>', models_manipulation.DeleteRecipeView.as_view(), name='remove_recipe'),
    path('products', models_manipulation.categories_and_products, name='products'),
    path('addProduct', models_manipulation.AddProduct.as_view(), name='addProduct'),

    path('api/', include('Recipes.api_urls')),

    path('register/', view_auth.register, name='register'),
    path('login/', view_auth.user_login, name='login'),
    path('logout/', view_auth.user_logout, name='logout'),
    path('admin/', admin.site.urls),
]
