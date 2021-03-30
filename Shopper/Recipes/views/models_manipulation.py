from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from Recipes.models import Recipe, Ingredient, Product, Category
from Recipes.forms import IngredientFormSet, RecipeForm, ProductFormSet
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class RecipeDetails(LoginRequiredMixin, DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'Recipes/RecDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empty_ing_text = ("Ten przepis nie ma jeszcze składników", )
        context['ingredients'] = Ingredient.objects.filter(recipe=self.get_object()) or empty_ing_text
        return context


class AddRecipe(LoginRequiredMixin, CreateView):
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


class UpdateRecipe(LoginRequiredMixin, UpdateView):
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


class DeleteRecipeView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('main')


class AddProduct(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category']
    template_name = 'Recipes/AddProduct.html'

    def get_success_url(self):
        return reverse('addProduct')


@login_required()
def categories_and_products(request):
    if request.method == 'POST':

        category_id = request.POST.get('parent')
        category = Category.objects.get(pk=category_id)
        user = request.user
        group = user.groups.first()
        formset = ProductFormSet(request.POST, request.FILES, instance=category)
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(reverse('products'))

    else:
        categories = Category.objects.all()
        form = ProductFormSet()
        context = {
            'categories': categories,
            'form': form,
        }

        return render(request, 'Recipes/categories_and_products.html', context)