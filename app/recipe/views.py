''' views for the recipe APIs '''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


# the model view set is a class that provides the basic CRUD operations
# for a model in the database
class RecipeViewSet(viewsets.ModelViewSet):
    ''' view for manage recipe API '''

    # the serializer class is the RecipeSerializer class
    # which will serialize the model data
    serializer_class = serializers.RecipeSerializer

    # the queryset variable is the queryset for the model
    queryset = Recipe.objects.all()

    # the authentication class is the TokenAuthentication class
    # which will require the user to be authenticated to access the API
    authentication_classes = (TokenAuthentication,)

    # the permission class is the IsAuthenticated class which
    # will require the user to be authenticated to access the API
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ''' return the recipes for the authenticated user '''

        # filter the queryset by the user and order by the id descending
        return self.queryset.filter(user=self.request.user).order_by('-id')
