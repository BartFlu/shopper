from celery import shared_task
from .models import Recipe, ShoppingListItem
from django.utils import timezone
from django.core.mail import send_mail


@shared_task
def send_mail_and_clear_baset(text: str, email: str):
    sended = True

    try:
        celery_send_mail(text, email)
    except Exception as ex:
        sended = False

    finally:
        if sended:
            mark_recipe_as_used_and_clear_the_basket()


def celery_send_mail(text: str, address):
    send_mail(
        'Lista zakupów',
        text,
        'pan_automat@yahoo.com',
        [address],
        fail_silently=False,
    )


def mark_recipe_as_used_and_clear_the_basket():
    recipes = Recipe.objects.filter(chosen=True)
    for r in recipes:
        r.last_used = timezone.now()
        r.chosen = False
        r.save()
    s = ShoppingListItem()
    s.delete_everything()




