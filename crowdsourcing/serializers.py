from rest_framework import serializers
from django.contrib.auth.models import User
from crowdusers.models import *
from rest_framework.authtoken.models import Token
import datetime as dt
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentImages
        fields = ['file']


class DeploymentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentImages
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    deployment_image = serializers.SerializerMethodField('dep_image')
    days_since_deployment = serializers.SerializerMethodField('days_since_dep')
    report_nature_values = serializers.SerializerMethodField('list_report_nature')

    def dep_image(self, obj):
        deployment_img_file = DeploymentImages.objects.filter(deployment_number=obj.deployment_number).first()
        image_serializer = ImageSerializer(instance=deployment_img_file)
        return image_serializer.data

    def days_since_dep(self, obj):
        total_days_since_deployment = ''
        date_format = '%Y-%m-%d'
        current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
        formatted_deployment_date = datetime.strptime(
            dt.datetime.strptime(obj.report_date, '%d.%m.%Y').strftime('%Y-%m-%d'), date_format)
        date_diff = current_date - formatted_deployment_date
        if date_diff.days < 1:
            total_days_since_deployment = 'today'
        if date_diff.days == 1:
            total_days_since_deployment = str(date_diff.days) + " day ago"
        if date_diff.days > 1:
            total_days_since_deployment = str(date_diff.days) + " days ago"
        return total_days_since_deployment

    def list_report_nature(self, obj):
        report_nature_list_from_string = obj.report_nature.split(',')
        report_nature_to_display = []
        for i in report_nature_list_from_string:
            report_nature = ReportNature.objects.get(pk=i).name
            report_nature_to_display.append(report_nature)
        return ', '.join(report_nature_to_display)

    class Meta:
        model = Deployment
        fields = ['id', 'report_brief_description', 'report_nature', 'report_full_description', 'reporter_background',
                  'deployment_location', 'latitude', 'longitude', 'report_date', 'report_time',
                  'report_time_frame', 'report_response_bodies', 'report_video_link', 'report_views',
                  'deployment_number', 'report_platform', 'created_date', 'user',
                  'deployment_image', 'days_since_deployment', 'report_nature_values']


class ReportNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportNature
        fields = '__all__'
