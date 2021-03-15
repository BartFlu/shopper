from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Recipe, Ingredient, ShoppingListItem, BasketEntry
from django.shortcuts import get_object_or_404
from .tasks import send_mail_and_clear_baset

# Create your views here.


# Main view

class MainView(ListView):
    model = Recipe
    paginate_by = 14

    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'


class MainViewFiltered(ListView):
    template_name = 'Recipes/main_view.html'
    paginate_by = 14
    context_object_name = 'recipes'

    def get_queryset(self):
        print(self.kwargs['tag'])
        return Recipe.objects.filter(tags__in=[self.kwargs['tag']])


# Basket View

class BasketView(ListView):
    model = BasketEntry
    paginate_by = 20
    context_object_name = 'entries'
    template_name = 'Recipes/basket_view.html'


# Basket manipulation methods

def add_to_basket(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    BasketEntry.create_entry(r)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_basket(request, pk):
    BasketEntry.delete_entry(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def convert_to_shopping_list(request):

    recipes = Recipe.objects.filter(chosen=True)
    for r in recipes:
        ingredients = Ingredient.objects.filter(recipe=r)
        for i in ingredients:
            shopping_item, created = ShoppingListItem.objects.get_or_create(type=i.type, unit=i.unit)
            shopping_item.quantity += i.quantity
            shopping_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Shopping list

class ShoppingListView(ListView):
    model = ShoppingListItem
    context_object_name = 'list'
    template_name = 'Recipes/shoppingList.html'

    def get_queryset(self):
        queryset = ShoppingListItem.objects.all().order_by('type__category')
        return queryset

# Shopping list manipulation

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

        return HttpResponseRedirect('main')


def make_shopping_list():
    text = ''
    lines = ShoppingListItem.objects.all()
    for line in lines:
        text = text + line.to_string() + '\n'
        if line.comments:
            text = text + 'Uwagi: ' + line.comments + '\n'
    return text


def add_comment_to_shopping_item(request, pk):
    if request.method == 'POST':

        item = ShoppingListItem.objects.get(pk=pk)
        item.comments = request.POST.get('comment')
        item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_shopping_list(request, pk):
    item = ShoppingListItem.objects.get(pk=pk)
    item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Recipe

class RecipeDetails(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'Recipes/RecDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.filter(recipe=self.get_object())
        return context