''' test for recipe api '''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

# url for the recipe API
RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    ''' return the recipe detail url '''

    # return the url for the recipe detail
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_get_recipe_detail(self):
        ''' test retrieving a recipe detail '''

        # create a recipe
        recipe = create_recipe(user=self.user)

        # get the recipe detail url
        url = detail_url(recipe.id)

        # get the recipe detail url
        res = self.client.get(url)

        # serialize the recipe
        serializer = RecipeDetailSerializer(recipe)

        # assert that the status code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # assert that the response data is the same as the serialized data
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        ''' test creating a recipe '''

        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'description': 'Delicious cheesecake',
            'link': 'http://test.com/recipe.pdf',
        }

        # post the payload to the recipes url
        res = self.client.post(RECIPES_URL, payload)

        # assert that the status code is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the Recipe
        recipe = Recipe.objects.get(id=res.data['id'])

        # assert that each field is the same as the payload
        for k, v in payload.items():

            # getattr() returns the value of the named attribute of an object
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_create_recipe_with_tags(self):
        ''' test creating a recipe with tags '''

        # create a Tag
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        payload = {
            'title': 'Avocado lime cheesecake',
            'time_minutes': 60,
            'description': 'Delicious cheesecake',
            'link': 'http://test.com/recipe.pdf',
            'tags': [{'name': 'Vegan'}, {'name': 'Dessert'}],
        }

        # post the payload to the recipes url
        res = self.client.post(RECIPES_URL, payload, format='json')

        # assert that the status code is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the Recipe
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        # assert that the tags are the same as the payload
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                user=self.user,
                name=tag['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        ''' test creating a recipe with existing tags '''

        # create a Tag
        tag = Tag.objects.create(user=self.user, name='Vegan')

        payload = {
            'title': 'Avocado lime cheesecake',
            'time_minutes': 60,
            'description': 'Delicious cheesecake',
            'link': 'http://test.com/recipe.pdf',
            'tags': [{'name': 'Vegan'}, {'name': 'Dessert'}],
        }

        # post the payload to the recipes url
        res = self.client.post(RECIPES_URL, payload, format='json')

        # assert that the status code is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the Recipe
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        # assert that the tags are the same as the payload
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                user=self.user,
                name=tag['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        ''' test creating a new tag on update '''

        # create a recipe
        recipe = create_recipe(user=self.user)

        payload = {'tags': [{'name': 'Vegan'}, {'name': 'Dessert'}]}

        # get the recipe detail url
        url = detail_url(recipe.id)

        # patch the payload to the recipe detail url
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_tag = Tag.objects.get(user=self.user, name='Dessert')
        self.assertIn(new_tag, recipe.tags.all())

    def test_update_recipe_assing_tags(self):
        ''' test assigning an existing tag when creating a recipe'''

        tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')

        # create a Recipe
        recipe = create_recipe(user=self.user)

        # add a tag to the Recipe
        recipe.tags.add(tag_breakfast)

        # create a new tag
        tag_lunch = Tag.objects.create(user=self.user, name='Lunch')

        payload = {'tags': [{'name': 'Lunch'}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())

    def test_clear_recipe_tags(self):
        ''' test clearing a recipe tags '''

        tag = Tag.objects.create(user=self.user, name='Breakfast')

        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)

        payload = {'tags': []}

        url = detail_url(recipe.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        ''' test creating a recipe with new ingredients '''

        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'description': 'Delicious cheesecake',
            'link': 'http://test.com/recipe.pdf',
            'ingredients': [{'name': 'Chocolate'}, {'name': 'Cheese'}],
        }

        # post the payload to the recipes url
        res = self.client.post(RECIPES_URL, payload, format='json')

        # assert that the status code is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the Recipe
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)

        # assert that the ingredients are the same as the payload
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                user=self.user,
                name=ingredient['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_ingredients(self):
        ''' test creating a recipe with existing ingredients '''

        # create an Ingredient
        ingredient = Ingredient.objects.create(user=self.user, name='Chocolat')

        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'description': 'Delicious cheesecake',
            'link': 'http://test.com/recipe.pdf',
            'ingredients': [{'name': 'Chocolate'}, {'name': 'Cheese'}],
        }

        # post the payload to the recipes url
        res = self.client.post(RECIPES_URL, payload, format='json')

        # assert that the status code is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the Recipe
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)

        # assert that the ingredients are the same as the payload
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                user=self.user,
                name=ingredient['name']
            ).exists()
            self.assertTrue(exists)
