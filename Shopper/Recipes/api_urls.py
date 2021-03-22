from django.urls import path, include
from Recipes import api_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tags', api_views.TagViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'products', api_views.ProductViewSet)
router.register(r'recipes', api_views.RecipeViewsSet)

urlpatterns = [

]

urlpatterns += router.urls
