from rest_framework import serializers
from django.contrib.auth.models import User
from crowdusers.models import *
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentImages
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Deployment
        fields = '__all__'
