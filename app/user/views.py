''' views for user API '''

from rest_framework import generics
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    ''' create a new user in the system '''

    # serializer class to be used in the view
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    ''' create a new auth token for user '''

    # serializer class to be used in the view
    serializer_class = AuthTokenSerializer

    # renderer classes to be used in the view
    # used to make the view browsable
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
