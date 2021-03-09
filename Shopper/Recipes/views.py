from django.shortcuts import render, reverse, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from .models import Recipe, Ingredient, Tag
from django.shortcuts import get_object_or_404
from .forms import IngredientForm, RecipeForm, TagForm
# Create your views here.


class MainView(ListView):
    model = Recipe
    paginate_by = 14
    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'


def add_to_basket(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    r.chosen = True
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_basket(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    r.chosen = False
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ChosenRecipes(ListView):
    model = Recipe
    paginate_by = 20
    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'

    def get_queryset(self):
        return Recipe.objects.filter(chosen=True)
