from django.shortcuts import render, reverse, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe, Ingredient, ShoppingList
from django.shortcuts import get_object_or_404
from .forms import IngredientForm, RecipeForm, TagForm
from .tasks import send_mail_and_clear_baset
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
    template_name = 'Recipes/basket_view.html'

    def get_queryset(self):
        return Recipe.objects.filter(chosen=True)


class RecipeDetails(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'Recipes/RecDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.filter(recipe=self.get_object())
        return context


def convert_to_shopping_list(request):

    recipes = Recipe.objects.filter(chosen=True)
    for r in recipes:
        ingredients = Ingredient.objects.filter(recipe=r)
        for i in ingredients:
            slist, created = ShoppingList.objects.get_or_create(type=i.type, unit=i.unit)
            slist.quantity += i.quantity
            slist.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ShoppingListView(ListView):
    model = ShoppingList
    context_object_name = 'list'
    template_name = 'Recipes/shoppingList.html'


def send_list(request):
    """
    TODO: form.clean_data?
    :param request:
    :return:
    """
    if request.method == 'POST':

        email = request.POST.get('email')
        text = make_shopping_list()
        send_mail_and_clear_baset.delay(text, email)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def make_shopping_list():
    text = ''
    lines = ShoppingList.objects.all()
    for line in lines:
        text = text + line.to_string() + '\n'
    return text
