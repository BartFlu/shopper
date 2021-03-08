from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='nazwa')
    category = models.ForeignKey(Category, verbose_name='kategoria', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    source = models.URLField(verbose_name='Źródło', blank=True)
    tags = models.ManyToManyField(Tag)
    added = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


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
