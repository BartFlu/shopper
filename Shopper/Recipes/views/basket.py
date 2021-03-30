from Recipes.models import Recipe, Ingredient, ShoppingList
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse


@login_required()
def add_to_basket(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    r.chosen = True
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def remove_from_basket(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    r.chosen = False
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class BasketView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 20
    context_object_name = 'recipes'
    template_name = 'Recipes/basket_view.html'

    def get_queryset(self):
        return Recipe.objects.filter(chosen=True)


@login_required()
def convert_to_shopping_list(request):

    recipes = Recipe.objects.filter(chosen=True)
    for r in recipes:
        ingredients = Ingredient.objects.filter(recipe=r)
        for i in ingredients:
            # sum up similar ingredients
            shopping_list_item, created = ShoppingList.objects.get_or_create(type=i.type, unit=i.unit)
            shopping_list_item.quantity += i.quantity
            shopping_list_item.save()
    return HttpResponseRedirect(reverse('shoppingList'))
