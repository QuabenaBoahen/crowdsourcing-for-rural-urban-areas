from django.http import JsonResponse
from django.shortcuts import render, redirect

from crowdsourcing.serializers import DeploymentSerializer, ImageSerializer
from .forms import *
from django.contrib import messages
from .utils import CrowdSourcingUtils


def index(request):
    context = {
        'index': 'true',
        'deployments': CrowdSourcingUtils.paginate_deployments(request, Deployment.objects.all())
    }
    return render(request, 'crowdusers/index.html', context)


def get_single_deployment_details(request, **kwargs):
    if request.is_ajax and request.method == "GET":
        dep_pk = kwargs.get('dep_pk', None)
        if dep_pk:
            try:
                single_deployment = Deployment.objects.get(pk=dep_pk)
                single_deployment_images = DeploymentImages.objects.filter(deployment_number=single_deployment.deployment_number).first()
                serializer = DeploymentSerializer(instance=single_deployment)
                image_serializer = ImageSerializer(instance=single_deployment_images)

                # update views for this deployment when someone views for the first time
                if not 'viewed_deployment_%s' % dep_pk in request.session:
                    request.session['viewed_deployment_%s' % dep_pk] = True
                    single_deployment.report_views += 1
                    single_deployment.save()
                return JsonResponse({"data": serializer.data, "images": image_serializer.data}, status=200)
            except Deployment.DoesNotExist:
                return JsonResponse({"status": '404', 'error': 'No deployment found with the id %s ' % dep_pk},
                                    status=400)
        else:
            return JsonResponse({"error": '403', 'message': 'Invalid id for deployment'})


def about(request):
    return render(request, 'crowdusers/about.html', {'about': 'true'})


def contact(request):
    return render(request, 'crowdusers/contact-us.html', {'contact': 'true'})


def deployment(request):
    report_nature = ReportNature.objects.all()
    context = {
        'report_nature': report_nature,
        'deployment': 'true'
    }
    return render(request, 'crowdusers/create-deployment.html', context)


def persist_deployment(request):
    if 'random_deployment_number' in request.session:
        random_deployment_number = request.session['random_deployment_number']
    form = DeploymentForm(request.POST, request.FILES)
    if form.is_valid():
        user_deployment = form.save(commit=False)
        user_deployment.deployment_number = random_deployment_number
        user_deployment.user = request.user
        user_deployment.report_platform = 'Web'
        user_deployment.save()
        messages.add_message(request, messages.SUCCESS, 'Your deployment has been created successfully')
    else:
        messages.add_message(request, messages.WARNING, form.errors)
    return redirect('crowdusers:deployment')


def persist_deployment_images(request, **kwargs):
    random_deployment_number = kwargs.get('rand_deployment_number')
    if not 'rdn_%s' % random_deployment_number in request.session:
        request.session['random_deployment_number'] = random_deployment_number
        request.session['rdn_%s' % random_deployment_number] = True
    form = DeploymentImagesForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.deployment_number = request.session['random_deployment_number']
        image.save()
        data = {'is_valid': True, 'name': image.file.name, 'url': image.file.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)