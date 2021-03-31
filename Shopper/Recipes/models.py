from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)


class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nazwa', unique=True)
    category = models.ForeignKey(Category, verbose_name='Kategoria', on_delete=models.DO_NOTHING,
                                 related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category']


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nazwa')
    source = models.URLField(verbose_name='Źródło', blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tagi', related_name='recipes')
    added = models.DateTimeField(auto_now_add=True)
    last_used = models.DateField(null=True, blank=True)
    chosen = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('main')

    def last_used_info(self):
        if not self.last_used:
            return 'Jeszcze nie wykorzystany'
        elif self.last_used >= date.today() - timedelta(days=7):
            return 'Używane w tym tygodniu'
        elif self.last_used >= date.today() - timedelta(days=14):
            return 'Używane w zeszłym tygodniu'
        elif self.last_used >= date.today() - timedelta(days=21):
            return 'Używane 2 tygodnie temu'
        else:
            return 'Używane ponad 2 tygodnie temu'


class Ingredient(models.Model):

    UNITS = [
        (1, 'litres'),
        (2, 'milliliters'),
        (3, 'grams'),
        (4, 'pieces'),


    ]

    type = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produkt')
    quantity = models.PositiveIntegerField(verbose_name='Ilość')
    unit = models.IntegerField(choices=UNITS, verbose_name='Miara')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} - {self.quantity} {self.get_unit_display()}'


class ShoppingList(models.Model):

    UNITS = [
        (1, 'litres'),
        (2, 'milliliters'),
        (3, 'grams'),
        (4, 'pieces'),

    ]

    type = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.IntegerField(choices=UNITS)
    comments = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f'{self.type} - {self.quantity} {self.get_unit_display()}'

    @staticmethod
    def delete_everything():
        ShoppingList.objects.all().delete()

    def to_string(self):
        return self.__str__()
