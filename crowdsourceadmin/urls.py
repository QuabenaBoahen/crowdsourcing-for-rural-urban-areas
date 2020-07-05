from django.urls import path
from .views import *

app_name = 'crowdsourceadmin'
urlpatterns = [
    path('', index, name='index'),
    path('deployments/', deployments, name='deployments'),
    path('users/', users, name='users'),
    path('users/update-status/<int:user_pk>/', update_user_status, name='update_user_status'),
]
