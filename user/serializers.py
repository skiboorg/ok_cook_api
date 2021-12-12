from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser import utils
from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings
from rest_framework.response import Response

# User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'fio',
            'date_joined',
            'total_spend',

        ]
class UserLineSerializer(serializers.ModelSerializer):
    users = UserShortSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = UserRefferalFirstLine
        fields = [
            'users'
        ]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'required': False,
                                  'allow_blank': True}}

# djoser/utils.py проыерка на регу соц сетей


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'email',
            "password",
            "used_ref_code"
            # settings.LOGIN_FIELD,
            #User._meta.pk.name,

        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        print(validated_data)
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if not validated_data['used_ref_code']:
                user.used_ref_code = '123123'
                user.save(update_fields=["used_ref_code"])
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user




