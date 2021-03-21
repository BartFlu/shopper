from celery import shared_task
from .models import Recipe, ShoppingList
from django.utils import timezone
from django.core.mail import send_mail


@shared_task
def send_mail_and_clear_baset(email: str):
    sended = True
    text = make_shopping_list()
    try:
        celery_send_mail(text, email)
    except Exception as ex:
        sended = False

    finally:
        if sended:
            mark_recipe_as_used_and_clear_the_basket_and_shopping_list()


def make_shopping_list():
    text = ''
    lines = ShoppingList.objects.all()
    for line in lines:
        text = text + line.to_string() + '\n'
        if line.comments:
            text = text + 'Uwagi: ' + line.comments + '\n'
    return text


def celery_send_mail(text: str, address):
    send_mail(
        'Lista zakupów',
        text,
        'pan_automat@yahoo.com',
        [address],
        fail_silently=False,
    )


def mark_recipe_as_used_and_clear_the_basket_and_shopping_list():
    recipes = Recipe.objects.filter(chosen=True)
    for r in recipes:
        r.last_used = timezone.now()
        r.chosen = False
        r.save()
    s = ShoppingList()
    s.delete_everything()




