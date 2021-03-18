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
from django.urls import path
from Recipes import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('/<tag>', views.MainViewFiltered.as_view(), name='main_filtered'),
    path('addToBasket/<int:pk>', views.add_to_basket, name='addToBasket'),
    path('removeFromBasket/<int:pk>', views.remove_from_basket, name='removeFromBasket'),
    path('basket', views.BasketView.as_view(), name='basket'),
    path('recipe/<int:pk>', views.RecipeDetails.as_view(), name='recipe'),
    path('toshoppinglist', views.convert_to_shopping_list, name='convert'),
    path('shoppingList', views.ShoppingListView.as_view(), name='shoppingList'),
    path('sendList', views.send_list, name='sendList'),
    path('add_comment/<int:pk>', views.add_comment_to_shopping_item, name='add_comment'),
    path('delete_shopping_item/<int:pk>', views.remove_from_shopping_list, name='removeFromList'),
    path('add_recipe', views.AddRecipe.as_view(), name='add_recipe'),
    path('update_recipe/<int:pk>', views.UpdateRecipe.as_view(), name='edit_recipe'),
    path('admin/', admin.site.urls),
]
