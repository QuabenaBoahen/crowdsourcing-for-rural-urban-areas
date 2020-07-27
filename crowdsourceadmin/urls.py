from django.urls import path
from .views import *

app_name = 'crowdsourceadmin'
urlpatterns = [
    path('', index, name='index'),
    path('deployments/', deployments, name='deployments'),
    path('users/', users, name='users'),
    path('response-bodies/', response_bodies, name='response_bodies'),
    path('persist-response-body/', persist_response_body, name='persist_response_body'),
    path('users/update-status/<int:user_pk>/', update_user_status, name='update_user_status'),
]
