''' tests for the ingredients api '''

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    ''' return ingredient detail url '''
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@test.com', password='test123'):
    ''' helper function to create a user '''
    return get_user_model().object.create_user(email, password)


class PublicIngredientsApiTests(TestCase):
    ''' test unauthenticated ingredients api requests '''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        ''' test that login is required to access the endpoint '''

        # make a get request to the ingredients url
        res = self.client.get(INGREDIENTS_URL)

        # check that the status code is 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    ''' test authenticated ingredients api requests '''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        ''' test retrieving a list of ingredients '''

        # create two ingredients
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        # make a get request to the ingredients url
        res = self.client.get(INGREDIENTS_URL)

        # get all the ingredients from the database
        ingredients = Ingredient.objects.all().order_by('-name')

        # serialize the Ingredient
        serializer = IngredientSerializer(ingredients, many=True)

        # check that the status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check that the response data is the same as the serialized data
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        ''' test that ingredients for the authenticated user are returned '''

        # create a second user
        user2 = create_user(email='test@test.com', password='test123')

        # create an ingredient for the second User
        Ingredient.objects.create(user=user2, name='Vinegar')

        # create an ingredient for the first User
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        # make a get request to the ingredients url
        res = self.client.get(INGREDIENTS_URL)

        # check that the status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check that the response data is a list with one item
        self.assertEqual(len(res.data), 1)

        # check that the response data is the same as the serialized data
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_update_ingredient(self):
        ''' test updating an ingredient '''

        # create an ingredient
        ingredient = Ingredient.objects.create(user=self.user, name='Cabbage')

        # create the payload
        payload = {'name': 'Cabbage'}

        # make a patch request to the ingredient detail url
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        # check that status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # get the ingredient from the database
        ingredient.refresh_from_db()

        # check that the ingredient name is the same as the payload
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ''' test deleting an ingredient '''

        # create an Ingredient
        ingredient = Ingredient.objects.create(user=self.user, name='Cabbage')

        # make a delete request to the ingredient detail url
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        # check that the status code is 204
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # check that the ingredient is not in the database
        exists = Ingredient.objects.filter(
            id=ingredient.id
        ).exists()

        self.assertFalse(exists)
