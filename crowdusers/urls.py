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
    path('deployments/single-deployment-details/<int:dep_pk>/', single_deployment_details, name="single_deployment_details_template"),
    path('forward-to-response-body/', forward_report_to_response_body, name='forward_report_to_response_body'),
    #path('deployments/location/<str:lat>/<str:lng>/', get_location_from_latlng, name="get_location_from_latlng"),
    path('create-deployment/persist-deployment-images/<int:rand_deployment_number>/', persist_deployment_images, name="persist_deployment_images"),
]