from django.contrib.auth.models import User
from django.db import models


class ReportNature(models.Model):
    name = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.name


class Deployment(models.Model):
    report_brief_description = models.CharField(max_length=200, blank=False)
    report_nature = models.CharField(max_length=15, blank=False)
    report_full_description = models.TextField(blank=False)
    reporter_background = models.CharField(max_length=25, blank=False)
    deployment_location = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=20, blank=False)
    longitude = models.CharField(max_length=20, blank=False)
    report_date = models.CharField(max_length=12, blank=False)
    report_time = models.CharField(max_length=12, blank=False)
    report_time_frame = models.CharField(max_length=120, blank=False)
    report_response_bodies = models.CharField(max_length=255, blank=True)
    report_video_link = models.CharField(max_length=255, blank=True)
    report_views = models.IntegerField(blank=True, default=0)
    deployment_number = models.CharField(max_length=10, blank=True)
    report_platform = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_brief_description

    class Meta:
        ordering = ['-created_date']


class DeploymentImages(models.Model):
    deployment_number = models.CharField(max_length=10, blank=False)
    file = models.ImageField(upload_to='deployment/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CustomUser(User):
    display_name = models.CharField(max_length=55, blank=True)


