''' serializers for recipe API '''

from rest_framework import serializers

from core.models import Recipe


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
        )

        # read only
        read_only_fields = ('id',)
