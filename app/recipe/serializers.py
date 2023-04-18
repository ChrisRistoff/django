''' serializers for recipe API '''

from rest_framework import serializers

from core.models import Recipe, Tag


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

    class Meta:

        model = Recipe

        # fields to be serialized
        fields = (
            'id',
            'title',
            'time_minutes',
            'link',
            'description',
            'tags',
        )

        # read only
        read_only_fields = ('id',)

    def create(self, validated_data):
        ''' create a new recipe '''

        # remove the tags from the validated data and
        # assign it to the tags variable so we can add it to the recipe
        tags = validated_data.pop('tags', [])

        # create the recipe excluding the tags
        recipe = Recipe.objects.create(**validated_data)

        # auth_user is the authenticated user that is creating the recipe
        auth_user = self.context['request'].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )

            # add the tag to the recipe
            recipe.tags.add(tag_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    ''' serializer for recipe details '''

    # override the Meta class
    class Meta(RecipeSerializer.Meta):

        model = Recipe

        # fields to be serialized
        fields = RecipeSerializer.Meta.fields + ('description',)
