from django.test import TestCase
from django.urls import reverse

from Recipes.models import Recipe, Tag, Category, Product, Ingredient, ShoppingList


class RecipesListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_recipes = 20

        for num in range(number_of_recipes):
            Recipe.objects.create(
                name=f'Test recipe {num}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_view_accessible_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.get(reverse('main'))
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(response.context['is_paginated'], True)
        self.assertTrue(len(response.context['recipes']) == 14)

    def test_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'Recipes/main_view.html')


# noinspection SpellCheckingInspection
class FilteredRecipesViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        t1, created = Tag.objects.get_or_create(tag='Obiad')
        t2, created = Tag.objects.get_or_create(tag='Mięso')

        r, created = Recipe.objects.get_or_create(name='Gotowane warzywa')
        r.tags.add(t1)
        r.save()

        r, created = Recipe.objects.get_or_create(name='Pieczone warzywa z kurczakiem')
        r.tags.add(t1, t2)
        r.save()

        Recipe.objects.create(name='Frytki')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/filtered/1')
        self.assertEqual(response.status_code, 200)

    def test_main_view_accessible_by_name(self):
        response = self.client.get(reverse('main_filtered', kwargs={'tag': 1}))
        self.assertEqual(response.status_code, 200)

    def test_filtration(self):
        response = self.client.get(reverse('main_filtered', kwargs={'tag': 1}))
        self.assertEqual(len(response.context['recipes']), 2)

    def test_correct_template(self):
        response = self.client.get(reverse('main_filtered', kwargs={'tag': 1}))
        self.assertTemplateUsed(response, 'Recipes/main_view.html')

    def test_context_data_filtered(self):
        response = self.client.get(reverse('main_filtered', kwargs={'tag': 1}))
        self.assertEqual(response.context['filtered'], 1)

    def test_advanced_view_url_exists_at_desired_location(self):
        response = self.client.get('/advancedFilter/')
        self.assertEqual(response.status_code, 200)

    def test_advanced_view_accessible_by_name(self):
        response = self.client.get(reverse('advanced_filter'))
        self.assertEqual(response.status_code, 200)


class BasketViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(name='basket')

    def test_mark_as_chosen(self):
        r = Recipe.objects.get(name='basket')
        self.client.get(reverse('addToBasket', kwargs={"pk": r.pk}))
        r = Recipe.objects.get(name='basket')
        self.assertEqual(r.chosen, True)

    def test_basket_context_object_name(self):
        r = Recipe.objects.get(name='basket')
        self.client.get(reverse('addToBasket', kwargs={"pk": r.pk}))
        response = self.client.get(reverse('basket'))
        self.assertTrue(response.context['recipes'])

    def test_unmark_as_chosen(self):
        r = Recipe.objects.get(name='basket')
        self.client.get(f'removeFromBasket/{r.id}')
        self.assertFalse(r.chosen)

    def test_basket_access_by_url(self):
        response = self.client.get('/basket')
        self.assertEqual(response.status_code, 200)

    def test_basket_access_by_name(self):
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)


class RecipeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(name='Detal')

    def test_detailview_accessible_by_url(self):
        r = Recipe.objects.get(name='Detal')
        response = self.client.get(f'/recipe/{r.id}')
        self.assertEqual(response.status_code, 200)

    def test_detailview_accessible_by_name(self):
        r = Recipe.objects.get(name='Detal')
        response = self.client.get(reverse('recipe', kwargs={"pk": r.id}))
        self.assertEqual(response.status_code, 200)

    def test_ingredients_in_context_data(self):
        r = Recipe.objects.get(name='Detal')
        response = self.client.get(f'/recipe/{r.id}')
        self.assertTrue(response.context['ingredients'])


class ShoppingListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='cTest')
        Product.objects.create(name='pTest', category=Category.objects.get(category='cTest'))
        Recipe.objects.create(name='rTest', chosen=True)
        Ingredient.objects.create(type=Product.objects.get(name='pTest'),
                                  quantity=15,
                                  unit=1,
                                  recipe=Recipe.objects.get(name='rTest'))

    def test_convert_to_shopping_list(self):
        self.client.get(reverse("convert"))
        shopping_item = ShoppingList.objects.first()
        self.assertIsNot(shopping_item, None)

    def test_shopping_list_access_by_url(self):
        response = self.client.get('/shoppingList')
        self.assertEqual(response.status_code, 200)

    def test_shopping_list_access_by_name(self):
        response = self.client.get(reverse('shoppingList'))
        self.assertEqual(response.status_code, 200)

    def test_context_object_name(self):
        self.client.get(reverse("convert"))
        response = self.client.get(reverse('shoppingList'))
        self.assertTrue(response.context['list'])

    def test_add_comment_to_shopping_item(self):
        self.client.get(reverse("convert"))
        shopping_item = ShoppingList.objects.first()
        self.client.post(f"/addComment/{shopping_item.id}", data={'comment': 'test_comment'})
        shopping_item = ShoppingList.objects.first()
        self.assertTrue(shopping_item.comments)

    def test_remove_from_shopping_list(self):
        self.client.get(reverse("convert"))
        shopping_item = ShoppingList.objects.first()
        self.client.get(f'/deleteShoppingItem/{shopping_item.id}')
        shopping_item = ShoppingList.objects.first()
        self.assertIsNone(shopping_item)





