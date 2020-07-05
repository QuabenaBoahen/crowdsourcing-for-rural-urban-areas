from django.urls import path
from .views import *

app_name = 'crowdusers'
urlpatterns = [
    path('', index, name="index"),
    path('about-us/', about, name="about"),
    path('contact-us/', contact, name="contact"),
    path('create-deployment/', deployment, name="deployment"),
    path('create-deployment/persist-deployment/', persist_deployment, name="persist_deployment"),
    path('deployments/<int:dep_pk>/', get_single_deployment_details, name="single_deployment_details"),
    path('create-deployment/persist-deployment-images/<int:rand_deployment_number>/', persist_deployment_images, name="persist_deployment_images"),
]