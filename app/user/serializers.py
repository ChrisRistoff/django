'''
serializers for the user api
'''

from django.contrib.auth import (
        get_user_model,
        authenticate,
        )
from django.utils.translation import ugettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    ''' serializer for the user object '''

    # Meta class is used to define the model and the fields to be used
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

    def update(self, instance, validated_data):
        ''' update a user and set the password correctly and return it '''

        # remove the password from the validated data
        password = validated_data.pop('password', None)

        # update the user with the validated data
        user = super().update(instance, validated_data)

        # check if the password is not None
        if password:

            # set the password for the user
            user.set_password(password)

            # save the user
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    ''' serializer for the user authentication object '''

    # email and password fields
    email = serializers.EmailField()
    password = serializers.CharField(
            style={'input_type': 'password'},
            trim_whitespace=False,
            )

    def validate(self, attrs):
        ''' validate and authenticate the user '''

        # get the email and password from the attrs dictionary
        email = attrs.get('email')
        password = attrs.get('password')

        # authenticate the user
        user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password,
                )

        # check if the user exists
        if not user:

            msg = _('Unable to authenticate with provided credentials')
            # raise a validation error with the message and a code
            raise serializers.ValidationError(msg, code='authentication')

        # check if the user is active
        attrs['user'] = user

        # return the user if the user is active
        return attrs
