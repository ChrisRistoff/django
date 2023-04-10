'''test for the django admin modifcations'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from ..models import User


class AdminSiteTests(TestCase):

    # needs to be called setUp
    def setUp(self):

        # create a client
        self.client = Client()

        # delete an existing user. This is to avoid the error
        # of the user already existing in the database
        try:
            superuser = get_user_model().object.get(email="admintest@test.com")
            superuser.delete()
        except User.DoesNotExist:
            pass

        # create a superuser
        self.admin_user = get_user_model().object.create_superuser(
                email="admintest@test.com",
                password="test123"
        )

        # force login the user to test the admin site
        # force_login is a helper function
        self.client.force_login(self.admin_user)

        # create a user to test the admin site
        self.user = get_user_model().object.create_user(
                email="usertest@test.com",
                password="test123",
                name="Test user full name"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""

        # reverse will generate the url for the list user page
        # admin:core_user_changelist is the name of the url it is builtin
        # self.client.get will send a get request to the url
        # and return the response
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        '''test the edit page for the user'''

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        '''test the create user page'''

        # /admin/core/user/add is the url for the create user page
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
