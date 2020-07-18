from django.contrib import admin
from .models import *


@admin.register(ReportNature)
class ReportNatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    pass


@admin.register(DeploymentImages)
class DeploymentImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
