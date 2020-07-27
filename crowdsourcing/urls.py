from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from .views import *


admin.site.site_header = 'Peda Reporter'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crowdusers.urls')),
    path('api/v1/', include('mobile_api.urls')),
    path('admin-site/', include('crowdsourceadmin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/activate/<str:username>/', Account.activate_user_account, name='activate_account'),
    path('accounts/reset-password/', Account.change_password, name="reset_password"),
    path('accounts/reset-password/send-email/', Account.send_password_reset_email, name="send_password_reset_email"),
    path('accounts/signup/', Account.as_view(), name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]
