''' url mapping for the recipe app '''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

# create a router
# this will automatically create the urls for the viewset
router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

# the app Name
app_name = 'recipe'

# the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
