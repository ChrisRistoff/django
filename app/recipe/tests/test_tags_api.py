''' tests for the tags api '''

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import RecipeTagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email="test@test.com", password="testpass123"):
    ''' Create and return a user '''

    return get_user_model().object.create_user(
            email=email, password=password)


class PublicTagsApiTest(TestCase):
    ''' Test unauthenticated API requests'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        ''' test auth is required for retrieving tags '''

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    ''' Test authenticated API requests '''

    def setUp(self):

        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        ''' test retrieving a list of tags '''

        # create 2 tags for the user
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Meat")

        # get all the tags from the database and store them in tags
        tags = Tag.objects.all().order_by('-name')

        # get the tags from the API and store them in res
        res = self.client.get(TAGS_URL)

        # serialize the tags and store them in serializer
        serializer = RecipeTagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        ''' test that tags returned are for the authenticated user '''

        # create a user
        user2 = create_user(email="test23@test.com")

        # create a tag for the user2
        Tag.objects.create(user=user2, name="Comfort")
        tag = Tag.objects.create(user=self.user, name="Meat")

        # get the tags from the API and store them in res
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
