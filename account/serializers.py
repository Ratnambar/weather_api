from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import fields
from django.http import request
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, Serializer


class SignupSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }


    def validate_password(self,value):
        validate_password(value)
        return value


    def create(self,validate_data):
        user = get_user_model()(**validate_data)
        user.set_password(validate_data['password'])
        user.save()
        return user



class LoginSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
