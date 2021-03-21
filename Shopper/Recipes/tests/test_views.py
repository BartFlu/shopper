from django.test import TestCase
from django.urls import reverse

from Recipes.models import Recipe, Tag


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
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['recipes']) == 14)

    def test_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'Recipes/main_view.html')


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

        r, created = Recipe.objects.get_or_create(name='Frytki')

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
        response = self.client.get('/advanced_filter/')
        self.assertEqual(response.status_code, 200)

    def test_advanced_view_accessible_by_name(self):
        response = self.client.get(reverse('advanced_filter'))
        self.assertEqual(response.status_code, 200)







