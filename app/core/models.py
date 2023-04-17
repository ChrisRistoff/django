'''
database models
'''

from django.conf import settings
from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# UserManager is a class that comes with django
# it is used to create a custom user model.
# it is used to create a user, create a superuser, create a staff user
class UserManager(BaseUserManager):
    '''manager for user profiles'''

    def create_user(self, email, password=None, **extra_field):
        '''create a new user profile'''
        if not email:
            raise ValueError('Users must have an email address')

        # normalize_email is a method that comes with django
        # it will convert the email to lowercase and remove any spaces
        # before and after the email address and return it as a string
        user = self.model(email=self.normalize_email(email), **extra_field)

        # set_password is a method that comes with django
        # it will hash the password and store it in the database
        # it will also set the password_changed field to the current date
        user.set_password(password)

        # save the user to the database using the _db attribute
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''create and save a new superuser with given details'''
        user = self.create_user(email, password)

        # is_superuser comes with django
        # used to check if the user is a superuser
        user.is_superuser = True

        # is_staff comes with django
        # check if the user is a staff member or not
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''user in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # required by django to create a custom user model
    # used to check if the user is active or not
    # use it to deactivate users instead of deleting them
    is_active = models.BooleanField(default=True)

    # required by django to create a custom user model
    # check if the user is a staff member or not.
    # give staff members access to the admin panel
    is_staff = models.BooleanField(default=False)

    # required by django to create a custom user model
    # we use it in the create_superuser etc methods and test cases
    object = UserManager()

    # field that will be used to login to the system
    # instead of the default username field that comes with django
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    ''' recipe object '''

    # the user that created the Recipe
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
