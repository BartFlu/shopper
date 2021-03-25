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
from Recipes import views, view_auth


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('filtered/<tag>', views.MainViewFiltered.as_view(), name='main_filtered'),
    path('advancedFilter/', views.advanced_filter_view, name='advanced_filter'),
    path('addToBasket/<int:pk>', views.add_to_basket, name='addToBasket'),
    path('removeFromBasket/<int:pk>', views.remove_from_basket, name='removeFromBasket'),
    path('basket', views.BasketView.as_view(), name='basket'),
    path('recipe/<int:pk>', views.RecipeDetails.as_view(), name='recipe'),
    path('updateRecipe/<int:pk>', views.UpdateRecipe.as_view(), name='edit_recipe'),
    path('addRecipe', views.AddRecipe.as_view(), name='add_recipe'),
    path('removeRecipe/<int:pk>', views.DeleteRecipeView.as_view(), name='remove_recipe'),
    path('products', views.categories_and_products, name='products'),
    path('toShoppinglist', views.convert_to_shopping_list, name='convert'),
    path('shoppingList', views.ShoppingListView.as_view(), name='shoppingList'),
    path('sendList', views.send_list, name='sendList'),
    path('addComment/<int:pk>', views.add_comment_to_shopping_item, name='add_comment'),
    path('deleteShoppingItem/<int:pk>', views.remove_from_shopping_list, name='removeFromList'),
    path('addProduct', views.AddProduct.as_view(), name='addProduct'),
    path('api/', include('Recipes.api_urls')),
    path('register/', view_auth.register, name='register'),
    path('login/', view_auth.user_login, name='login'),
    path('admin/', admin.site.urls),
]
