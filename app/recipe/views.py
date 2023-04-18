''' views for the recipe APIs '''

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


# the model view set is a class that provides the basic CRUD operations
# for a model in the database
class RecipeViewSet(viewsets.ModelViewSet):
    ''' view for manage recipe API '''

    # serialize the model data
    serializer_class = serializers.RecipeSerializer

    # the queryset variable is the queryset for the model
    queryset = Recipe.objects.all()

    # will require the user to be authenticated to access the API
    authentication_classes = (TokenAuthentication,)

    # require the user to be authenticated to access the API
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ''' return the recipes for the authenticated user '''

        # filter the queryset by the user and order by the id descending
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        ''' return the serializer class for request '''

        if self.action == 'list':
            return serializers.RecipeDetailSerializer

        # default serializer class
        return self.serializer_class

    def perform_create(self, serializer):
        ''' create a new recipe '''

        # modify the behavior of the create method to set the user
        # to the authenticated user before saving the object to the database
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    ''' view for manage tags API '''

    # serialize the model data
    serializer_class = serializers.RecipeTagSerializer

    # the queryset variable is the queryset for the model
    queryset = Tag.objects.all()

    # will require the user to be authenticated to access the API
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ''' return the tags for the authenticated user '''

        # filter the queryset by the user and order by the id descending
        return self.queryset.filter(user=self.request.user).order_by('-name')
