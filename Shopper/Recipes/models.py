from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from datetime import date, timedelta


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='nazwa')
    category = models.ForeignKey(Category, verbose_name='kategoria', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    source = models.URLField(verbose_name='Źródło', blank=True)
    tags = models.ManyToManyField(Tag)
    added = models.DateTimeField(auto_now_add=True)
    last_used = models.DateField(null=True, blank=True)
    chosen = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
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

    type = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.IntegerField(choices=UNITS)
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

    def delete_everything(self):
        ShoppingList.objects.all().delete()


    def to_string(self):
        return self.__str__()




