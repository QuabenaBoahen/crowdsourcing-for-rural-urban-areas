from rest_framework import viewsets
from crowdusers.models import *
from crowdsourcing.serializers import *
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from crowdusers.utils import CrowdSourcingUtils
from rest_framework.response import Response


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if User.objects.filter(email=email).exists():
            return Response({"message": 'An account with email %s ' % email +
                                 ' already exist. If this is your email please login or reset your password on the web app', "status": "401", "error": "true"}, status=200)
        elif User.objects.filter(username=username).exists():
            return Response({"message": 'An account with username %s ' % username +
                                 ' already exist. Please choose a different username', "status": "402", "error": "true"},
                                status=200)
        else:
            user = User.objects.create_user(email=email,
                                            username=username,
                                            password=password, is_active=True)
            return Response({"message": 'Account created successfully', "status": "200", "error": "false"},
                                status=200)


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'], url_path='single_deployment_details')
    def get_single_deployment_details(self, request):
        dep_pk = request.query_params.get('dep_pk', None)
        if dep_pk:
                try:
                    single_deployment = Deployment.objects.get(pk=dep_pk)
                    single_deployment_images = DeploymentImages.objects.filter(
                        deployment_number=single_deployment.deployment_number).first()
                    days_since_deployment = CrowdSourcingUtils.days_since_deployment(single_deployment.report_date)
                    serializer = DeploymentSerializer(instance=single_deployment)
                    image_serializer = ImageSerializer(instance=single_deployment_images)

                    # update views for this deployment when someone views for the first time
                    if not 'viewed_deployment_%s' % dep_pk in request.session:
                        request.session['viewed_deployment_%s' % dep_pk] = True
                        single_deployment.report_views += 1
                        single_deployment.save()
                    return JsonResponse({"data": serializer.data, "images": image_serializer.data,
                                         'days_since_deployment': days_since_deployment}, status=200)
                except Deployment.DoesNotExist:
                    return JsonResponse({"status": '404', 'error': 'No deployment found with the id %s ' % dep_pk},
                                        status=400)
        else:
            return JsonResponse({"error": '403', 'message': 'Invalid id for deployment'})

    @action(detail=False, methods=['POST'], url_path='create_deployment')
    def create_deployment(self, request):
        report_brief_description = request.data.get('report_brief_description', None)
        report_nature = request.data.get('report_nature', None)
        report_full_description = request.data.get('report_full_description', None)
        reporter_background = request.data.get('reporter_background', None)
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)
        report_date = request.data.get('report_date', None)
        report_time = request.data.get('report_time', None)
        report_time_frame = request.data.get('report_time_frame', None)
        report_response_bodies = request.data.get('report_response_bodies', None)
        report_video_link = request.data.get('report_video_link', None)
        print("data ", report_nature)
        return JsonResponse({"status": '200', 'data': report_nature})


class ReportNatureViewSet(viewsets.ModelViewSet):
    queryset = ReportNature.objects.all()
    serializer_class = ReportNatureSerializer
    permission_classes = (AllowAny,)
