from Recipes.models import ShoppingList
from Recipes.tasks import send_mail_and_clear_basket
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, reverse


class ShoppingListView(LoginRequiredMixin, ListView):
    model = ShoppingList
    context_object_name = 'list'
    template_name = 'Recipes/shoppingList.html'

    def get_queryset(self):
        queryset = ShoppingList.objects.all().order_by('type__category')
        return queryset


@login_required()
def send_list(request):
    """
    :param request:
    :return:
    """
    # todo use django email form
    if request.method == 'POST':

        email = request.POST.get('email')
        send_mail_and_clear_basket.delay(email)

        return HttpResponseRedirect(reverse('main'))


@login_required()
def add_comment_to_shopping_item(request, pk):
    if request.method == 'POST':

        item = ShoppingList.objects.get(pk=pk)
        item.comments = request.POST.get('comment')
        item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def remove_from_shopping_list(request, pk):
    item = ShoppingList.objects.get(pk=pk)
    item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
