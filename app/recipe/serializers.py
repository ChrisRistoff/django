''' serializers for recipe API '''

from rest_framework import serializers

from core.models import Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    ''' serializers for recipes '''

    class Meta:

        model = Recipe

        # fields to be serialized
        fields = (
            'id',
            'title',
            'time_minutes',
            'link',
            'description',
        )

        # read only
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    ''' serializer for recipe details '''

    # override the Meta class
    class Meta(RecipeSerializer.Meta):

        model = Recipe

        # fields to be serialized
        fields = RecipeSerializer.Meta.fields + ('description',)


class RecipeTagSerializer(serializers.ModelSerializer):
    ''' serializer for recipe tags '''

    class Meta:

        # model to be serialized
        model = Tag

        # fields to be serialized
        fields = ('id', 'name')

        # read only
        read_only_fields = ('id',)
