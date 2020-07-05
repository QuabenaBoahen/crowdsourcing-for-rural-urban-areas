from rest_framework import serializers
from django.contrib.auth.models import User
from crowdusers.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentImages
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Deployment
        fields = '__all__'
