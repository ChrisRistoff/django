''' views for user API '''

from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    ''' create a new user in the system '''

    # serializer class to be used in the view
    serializer_class = UserSerializer
