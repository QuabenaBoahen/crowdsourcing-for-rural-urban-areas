from django.shortcuts import render, redirect
from crowdusers.forms import *
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
def response_bodies(request):
    context = {
        'response_bodies': CustomUser.objects.all().order_by('-date_joined'),
        'form': ResponseBodyForm()
    }
    return render(request, 'crowdsourceadmin/response-bodies.html', context)


@login_required
def persist_response_body(request):
    form = ResponseBodyForm(request.POST)
    if form.is_valid():
        # check to see if response body already exist. If it exists we want to update else we'll create a new body
        pk = request.POST.get('id')
        if pk != 'None':
            resp_body_instance = CustomUser.objects.get(pk=pk)
            form = ResponseBodyForm(request.POST, instance=resp_body_instance)
            messages.add_message(request, messages.SUCCESS,
                                 'Response body with name "%s' % resp_body_instance.display_name + '" has been updated')
            form.save()
        else:
            if CustomUser.objects.filter(display_name=form.cleaned_data['display_name']).exists():
                messages.add_message(request, messages.ERROR,
                                     'A response body with name %s ' % form.cleaned_data['display_name'] +
                                     ' already exist. Please specify a different name')
            else:
                CustomUser.objects.create(**form.cleaned_data)
                #User.objects.create(username=form.cleaned_data['display_name'], password=form.cleaned_data['password'],
                                    #email=form.cleaned_data['email'], is_active=True)
                messages.add_message(request, messages.SUCCESS,
                                 'Response body with name "%s' % form.cleaned_data['display_name'] + '" has been created')
    else:
        messages.add_message(request, messages.ERROR,
                             form.errors)
    return redirect('crowdsourceadmin:response_bodies')


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

