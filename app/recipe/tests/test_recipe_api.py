''' test for recipe api '''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

# url for the recipe API
RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    ''' create and return a recipe '''

    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'description': 'Sample description',
        'link': 'http://test.com/recipe.pdf',
    }

    # update the defaults with the params
    defaults.update(params)

    # create the Recipe
    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeApiTests(TestCase):
    ''' test unauthenticated API requests '''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        ''' test that authentication is required '''

        # get the recipes url
        res = self.client.get(RECIPES_URL)

        # assert that the status code is 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    ''' test authenticated API requests '''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test@test.com',
            'testpass'
        )

        # authenticate the user
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        ''' test retrieving a list of recipes '''

        # create recipes
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # get the recipes url
        res = self.client.get(RECIPES_URL)

        # get the recipes
        recipes = Recipe.objects.all().order_by('-id')

        # serialize the recipes
        serializer = RecipeSerializer(recipes, many=True)

        # assert that the status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # assert that the response data is the same as the serialized data
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        ''' test retrieving recipes for user '''

        # create a user
        user2 = get_user_model().object.create_user(
            'test2@test.com',
            'testpass'
        )

        # create a recipe for the user
        create_recipe(user=user2)

        # create a recipe for the user
        create_recipe(user=self.user)

        # get the recipes url
        res = self.client.get(RECIPES_URL)

        # get the Recipe
        recipes = Recipe.objects.filter(user=self.user)

        # serialize the Recipe
        serializer = RecipeSerializer(recipes, many=True)

        # assert that the status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # assert that the response data is the same as the serialized data
        self.assertEqual(res.data, serializer.data)
