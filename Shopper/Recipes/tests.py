from django.test import TestCase
from .models import Tag, Category, Product, Recipe, Ingredient, ShoppingList
from django.utils import timezone
# Create your tests here.


class TagTestCase(TestCase):
    def testTag(self):
        tag = Tag(tag='Kolacja')
        self.assertEqual(tag.tag, 'Kolacja')


class CategoryTestCase(TestCase):
    def testCategory(self):
        cat = Category(category='Warzywa')
        self.assertEqual(cat.category, 'Warzywa')


class ProductTestCase(TestCase):
    def testProduct(self):
        cat = Category(category='Warzywa')
        p = Product(name='Marchewka', category=cat)
        self.assertEqual(p.name, 'Marchewka')
        self.assertEqual(p.category, cat)


class RecipeTestCase(TestCase):
    def testRecipe(self):
        t = tag = Tag(tag='Kolacja')
        t.save()
        r = Recipe(name='Naleśniki',
                   source='http://www.kwestiasmaku.com/kuchnia_polska/nalesniki/nalesniki.html',
                   added=timezone.now())
        r.save()
        r.tags.add(t)
        self.assertEqual(r.name, 'Naleśniki')
        self.assertEqual(r.source, 'http://www.kwestiasmaku.com/kuchnia_polska/nalesniki/nalesniki.html')
        self.assertIsNot(r.tags, False)
        self.assertEqual(r.chosen, False)


class IngredientTestCase(TestCase):
    def testIngredient(self):
        r = Recipe(name='Naleśniki',
                   source='http://www.kwestiasmaku.com/kuchnia_polska/nalesniki/nalesniki.html',
                   added=timezone.now())
        p = Product(name='Mleko')
        ing = Ingredient(type=p, quantity=2, unit=1, recipe=r)
        self.assertEqual(ing.type, p)
        self.assertEqual(ing.recipe, r)
        self.assertEqual(ing.quantity, 2)


class ShoppingListTestCase(TestCase):
    def testShoppingList(self):
        p = Product(name='Mleko')
        shopl = ShoppingList(type=p, quantity=2, unit=1)
        self.assertEqual(shopl.type, p)
        self.assertEqual(shopl.quantity, 2)

    def testToString(self):
        p = Product(name='Mleko')
        shopl = ShoppingList(type=p, quantity=2, unit=1)
        desc = shopl.to_string()
        self.assertIsInstance(desc, str)

    def testClearTable(self):
        c = Category(category='nabiał')
        c.save()
        p = Product(name='Mleko', category=c)
        p.save()
        shopl = ShoppingList(type=p, quantity=2, unit=1)
        shopl.save()
        s = ShoppingList.objects.first()
        self.assertEqual(s, shopl)
        shopl.delete_everything()
        s = ShoppingList.objects.first()
        self.assertIsNone(s)




