''' serializers for recipe API '''

from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    ''' serializer for ingredients '''

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeTagSerializer(serializers.ModelSerializer):
    ''' serializer for recipe tags '''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ''' serializers for recipes '''

    # the tags field is a many to many field
    # so we need to specify the serializer to use
    # for the tags field and set the many to True
    tags = RecipeTagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:

        model = Recipe

        # fields to be serialized
        fields = (
            'id',
            'title',
            'time_minutes',
            'link',
            'description',
            'instructions',
            'tags',
            'ingredients',
        )

        # read only
        read_only_fields = ('id',)

    def _get_or_create_tags(self, tags, recipe):
        ''' handle getting or creating tags '''
        auth_user = self.context['request'].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )

            # add the tag to the recipe
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        ''' handle getting or creating ingredients '''
        auth_user = self.context['request'].user

        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient
            )

            # add the ingredient to the recipe
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        ''' create a new recipe '''

        # remove the tags from the validated data and
        # assign it to the tags variable so we can add it to the recipe
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        # create the recipe excluding the tags
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        # auth_user is the authenticated user that is creating the recipe
        return recipe

    def update(self, instance, validated_data):
        ''' update a recipe '''

        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    ''' serializer for recipe details '''

    # override the Meta class
    class Meta(RecipeSerializer.Meta):

        model = Recipe

        # fields to be serialized
        fields = RecipeSerializer.Meta.fields + ('description',)
