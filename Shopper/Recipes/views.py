from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Recipe, Ingredient, ShoppingList, Product, Tag
from django.shortcuts import get_object_or_404
from .tasks import send_mail_and_clear_baset
from .forms import IngredientFormSet, RecipeForm, FilterForm
from django.urls import reverse_lazy, reverse
from django.db import transaction
from .documents import RecipeDocument
from .custom_sql import chain_filters


class MainView(ListView):
    model = Recipe
    paginate_by = 14

    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'


class MainViewFiltered(ListView):
    template_name = 'Recipes/main_view.html'
    paginate_by = 14
    context_object_name = 'recipes'

    # todo zmodyfikować context tak żeby dodać do niego 'filtered':True

    def get_queryset(self):
        return Recipe.objects.filter(tags__in=[self.kwargs['tag']])


def advance_filter_view(request):

    if request.method == 'POST':
        phrase = request.POST.get('Recipe_name', None)
        if phrase:
            el_results = RecipeDocument.search().query('match', name=phrase)
            pks = [x.id for x in el_results]

            results = Recipe.objects.filter(pk__in=pks)

            tag_form = FilterForm()
            tags = Tag.objects.all()

            return render(request, template_name='Recipes/advance_filter.html', context={'form': tag_form,
                                                                                         'tags': tags,
                                                                                         'results': results
                                                                                         })

        else:

            tag_form = FilterForm(request.POST)
            if tag_form.is_valid():
                search_tags = [x for x in tag_form.cleaned_data.get('Tags')]
                results = None
                for tag in search_tags:
                    results = Recipe.objects.filter(tags=tag)

                tag_form = FilterForm()
                tags = Tag.objects.all()

                return render(request, template_name='Recipes/advance_filter.html', context={'form': tag_form,
                                                                                             'tags': tags,
                                                                                             'results': results
                                                                                             })
    else:
        form = FilterForm()
        tags = Tag.objects.all()

        return render(request, template_name='Recipes/advance_filter.html', context={'form': form,
                                                                                     'tags': tags,
                                                                                     })


# def advance_filter_view(request):
#
#     if request.method == 'POST':
#         form = FilterForm(request.POST)
#         if form.is_valid():
#             tags = [x for x in form.cleaned_data.get('Tags')]
#             print(type(tags[0]))
#
#
#         recipes = Recipe.objects.all()
#         tags = Tag.objects.all()
#         return render(request, template_name='Recipes/advance_filter.html', context={'recipes': recipes,
#                                                                                      'tags': tags,
#                                                                                      'form': form})
#     else:
#
#         form = FilterForm()
#         recipes = Recipe.objects.all()
#         tags = Tag.objects.all()
#         return render(request, template_name='Recipes/advance_filter.html', context={'recipes': recipes,
#                                                                                      'tags': tags,
#                                                                                      'form': form})


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


class BasketView(ListView):
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
    return HttpResponseRedirect(reverse('shoppingList'))


class ShoppingListView(ListView):
    model = ShoppingList
    context_object_name = 'list'
    template_name = 'Recipes/shoppingList.html'

    def get_queryset(self):
        queryset = ShoppingList.objects.all().order_by('type__category')
        return queryset


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

        return HttpResponseRedirect(reverse('main'))


def make_shopping_list():
    text = ''
    lines = ShoppingList.objects.all()
    for line in lines:
        text = text + line.to_string() + '\n'
        if line.comments:
            text = text + 'Uwagi: ' + line.comments + '\n'
    return text


def add_comment_to_shopping_item(request, pk):
    if request.method == 'POST':

        item = ShoppingList.objects.get(pk=pk)
        item.comments = request.POST.get('comment')
        item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_shopping_list(request, pk):
    item = ShoppingList.objects.get(pk=pk)
    item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class AddRecipe(CreateView):
    model = Recipe
    template_name = 'Recipes/AddRecipe.html'
    form_class = RecipeForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(AddRecipe, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredients'] = IngredientFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        with transaction.atomic():
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(AddRecipe, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe', kwargs={'pk': self.object.pk})


class UpdateRecipe(UpdateView):
    model = Recipe
    template_name = 'Recipes/AddRecipe.html'
    form_class = RecipeForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(UpdateRecipe, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST, instance=self.object)
        else:
            data['ingredients'] = IngredientFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        with transaction.atomic():
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(UpdateRecipe, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe', kwargs={'pk': self.object.pk})


class AddProduct(CreateView):
    model = Product
    fields = ['name', 'category']
    template_name = 'Recipes/AddProduct.html'

    def get_success_url(self):
        return reverse('addProduct')

