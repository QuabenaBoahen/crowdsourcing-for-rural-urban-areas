from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register('users', UsersViewSet)
router.register('deployments', DeploymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', obtain_auth_token),
]