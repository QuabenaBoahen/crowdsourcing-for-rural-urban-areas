from django.shortcuts import render, redirect
from crowdusers.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta


@login_required
def index(request):
    context = {
        'total_users': User.objects.count(),
        'total_deployments': Deployment.objects.count(),
        'todays_deployments': Deployment.objects.filter(created_date__gte=datetime.now() - timedelta(days=1)).count(),
    }
    return render(request, 'crowdsourceadmin/index.html', context)


@login_required
def deployments(request):
    context = {
        'deployments': Deployment.objects.all()
    }
    return render(request, 'crowdsourceadmin/deployments.html', context)


@login_required
def users(request):
    context = {
        'users': User.objects.all().order_by('-date_joined'),
    }
    return render(request, 'crowdsourceadmin/users.html', context)


@login_required
def update_user_status(request, **kwargs):
    try:
        pk = kwargs.get('user_pk')
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Active status of "%s' % user.username + '" has been updated to %s ' % user.is_active)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR,
                             "We couldn't find an account for the user with an id of %s '" % pk + "'")
    return redirect('crowdsourceadmin:users')
