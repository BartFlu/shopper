from Recipes.models import Recipe, Tag
from Recipes.forms import FilterForm
from Recipes.documents import RecipeDocument
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class MainView(ListView):
    model = Recipe
    paginate_by = 14
    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'


class MainViewFiltered(ListView):
    paginate_by = 14
    context_object_name = 'recipes'
    template_name = 'Recipes/main_view.html'

    def get_queryset(self):
        return Recipe.objects.filter(tags__in=[self.kwargs['tag']])

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['filtered'] = 1
        return data


@login_required()
def advanced_filter_view(request):

    if request.method == 'POST':
        tag_form = FilterForm(request.POST)
        results = None
        tags = Tag.objects.all()

        # To distinguish forms check if 'Recipe_name' in post data
        phrase = request.POST.get('Recipe_name', None)
        if phrase:
            try:
                el_results = RecipeDocument.search().query('match', name=phrase)
                r_ids = [x.id for x in el_results]  # Elastic store only names and ids
                results = Recipe.objects.filter(pk__in=r_ids)  # to provide full functionality load from db
            except ConnectionError:
                results = Recipe.objects.filter(name__contains=phrase)

            tag_form = FilterForm()
            tags = Tag.objects.all()

        else:  # search by tags
            if tag_form.is_valid():
                search_tags = [x for x in tag_form.cleaned_data.get('Tags')]

                for tag in search_tags:  # cascade filtering to match only these records that match all tags
                    results = Recipe.objects.filter(tags=tag)

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
