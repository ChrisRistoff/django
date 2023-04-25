''' views for the recipe APIs '''

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Recipe, Tag, Ingredient
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

        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        # default serializer class
        return self.serializer_class

    def perform_create(self, serializer):
        ''' create a new recipe '''

        # modify the behavior of the create method to set the user
        # to the authenticated user before saving the object to the database
        serializer.save(user=self.request.user)

    # create a custom action for the viewset to upload an image
    # we use method POST to upload the image and the detail=True
    # to specify that the action is for a single object
    # the url_path is the url to access the action
    @action(methods=['POST'], detail=True, url_path='upload-image')
    # the pk is the primary key of the object
    # the request is the request object
    # pk is the primary key of the object to upload the image
    def upload_image(self, request, pk=None):
        ''' upload an image to a recipe '''

        # get the recipe object
        recipe = self.get_object()

        # get the serializer class
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            # save the serializer
            serializer.save()

            # return the serializer data
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    ''' base view for manage recipe attributes '''

    # will require the user to be authenticated to access the API
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ''' return the ingredients for the authenticated user '''

        # filter the queryset by the user and order by the id descending
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):

    ''' view for manage tags API '''

    # serialize the model data
    serializer_class = serializers.RecipeTagSerializer

    # the queryset variable is the queryset for the model
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    ''' view for manage ingredients API '''

    # serialize the model data
    serializer_class = serializers.IngredientSerializer

    # the queryset variable is the queryset for the model
    queryset = Ingredient.objects.all()
