# test for models

from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@test.com", password="test123"):
    ''' helper function to create a user '''
    return get_user_model().object.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'

        # create a user with the email and password from above
        # and store it in the user variable
        user = get_user_model().object.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        # list of lists with input and expected output for the test
        sample_emails = [
                ['test1@TEST.com', 'test1@test.com'],
                ['Test2@EXAmple.com', 'Test2@example.com'],
                ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
                ['test4@example.COM', 'test4@example.com'],
                ]

        for email, expected in sample_emails:

            # create a user with the email from the list and a default password
            user = get_user_model().object.create_user(email, 'test123')

            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        '''test creating user with no email raises error'''

        with self.assertRaises(ValueError):
            get_user_model().object.create_user("", 'test123')

    def test_create_new_superuser(self):
        '''test creating a new superuser'''

        user = get_user_model().object.create_superuser(
            'test@test.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        ''' test creating a recipe '''

        # create a User
        user = get_user_model().object.create_user(
            'test@test.com',
            'test123',
        )

        # create a Recipe
        recipe = models.Recipe.objects.create(
            user=user,
            title='Steak and mushroom sauce',
            time_minutes=5,
            description='How to make a delicious steak and mushroom sauce',
        )

        # check that the recipe has been created
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        ''' test creating a tag '''

        # create a User
        user = create_user()

        # create a Tag
        tag = models.Tag.objects.create(
            user=user,
            name='Vegetarian',
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        ''' test creating an ingredient '''

        # create a User
        user = create_user()

        # create an Ingredient
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)

    # @patch is a decorator that replaces the function with a mock function
    # so that we can control the output of the function and test it
    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        ''' test that image is saved in the correct location '''

        # mock the uuid function
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        # create a path for the image
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        # check that the path is correct
        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
