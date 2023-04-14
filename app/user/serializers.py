'''
serializers for the user api
'''

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    ''' serializer for the user object '''

    # Meta class is used to define the model and the fields to be used in the serializer
    class Meta:

        model = get_user_model()

        # list of fields to be used in the serializer and their order
        fields = ['email', 'password', 'name']

        # extra keyword arguments for the fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        ''' create a new user with encrypted password and return it '''

        # creating a new user with the create_user method
        return get_user_model().object.create_user(**validated_data)
