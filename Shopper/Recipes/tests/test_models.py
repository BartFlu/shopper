from django.test import TestCase
from Recipes.models import Recipe, Tag, Category, Product, Ingredient
from datetime import date, timedelta


class RecipeAndIngredientsTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        r, created = Recipe.objects.get_or_create(name='test_recipe2')
        c, created = Category.objects.get_or_create(category='test_category2')
        p, created = Product.objects.get_or_create(name='test_product2', category=c)
        Ingredient.objects.create(type=p, quantity=15, unit=1, recipe=r)



    def test_name_label(self):
        r = Recipe.objects.get(pk=1)
        name_label = r._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Nazwa')

    def test_source_name(self):
        r = Recipe.objects.get(pk=1)
        source_label = r._meta.get_field('source').verbose_name
        self.assertEqual(source_label, 'Źródło')

    def test_tags_name(self):
        r = Recipe.objects.get(pk=1)
        tags_label = r._meta.get_field('tags').verbose_name
        self.assertEqual(tags_label, 'Tagi')

    def test_absolute_url(self):
        r = Recipe.objects.get(pk=1)
        self.assertEqual(r.get_absolute_url(), '/')

    def test_last_used_never(self):
        r = Recipe.objects.get(pk=1)
        self.assertEqual(r.last_used_info(), 'Jeszcze nie wykorzystany')

    def test_last_used_this_week(self):
        r = Recipe.objects.get(pk=1)
        r.last_used = date.today()
        r.save()
        self.assertEqual(r.last_used_info(), 'Używane w tym tygodniu')

    def test_last_used_last_week(self):
        r = Recipe.objects.get(pk=1)
        r.last_used = (date.today() - timedelta(days=8))
        r.save()
        self.assertEqual(r.last_used_info(), 'Używane w zeszłym tygodniu')

    def test_last_used_two_weeks(self):
        r = Recipe.objects.get(pk=1)
        r.last_used = (date.today() - timedelta(days=15))
        r.save()
        self.assertEqual(r.last_used_info(), 'Używane 2 tygodnie temu')

    def test_last_used_two_weeks_and_more(self):
        r = Recipe.objects.get(pk=1)
        r.last_used = (date.today() - timedelta(days=22))
        r.save()
        self.assertEqual(r.last_used_info(), 'Używane ponad 2 tygodnie temu')

    def test_added_automated_input(self):
        r = Recipe.objects.get(pk=1)
        self.assertIsNot(r.added, None)

    def test_ingredient_type_label(self):
        i = Ingredient.objects.get(pk=1)
        label = i._meta.get_field('type').verbose_name
        self.assertEqual(label, 'Produkt')

    def test_ingredient_quantity_label(self):
        i = Ingredient.objects.get(pk=1)
        label = i._meta.get_field('quantity').verbose_name
        self.assertEqual(label, 'Ilość')

    def test_ingredient_unit_label(self):
        i = Ingredient.objects.get(pk=1)
        label = i._meta.get_field('unit').verbose_name
        self.assertEqual(label, 'Miara')


class ProductTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        c, created = Category.objects.get_or_create(category='test_category')
        Product.objects.create(name='test_product', category=c)

    def test_name_label(self):
        p = Product.objects.get(pk=1)
        name_label = p._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Nazwa')

    def test_category_label(self):
        p = Product.objects.get(pk=1)
        category_label = p._meta.get_field('category').verbose_name
        self.assertEqual(category_label, 'Kategoria')



