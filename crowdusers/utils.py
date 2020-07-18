from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime as dt
from datetime import datetime


class CrowdSourcingUtils:
    def paginate_deployments(request, object_list):
        page = request.GET.get('page', 1)
        paginator = Paginator(object_list, 4)
        try:
            deployments = paginator.page(page)
        except PageNotAnInteger:
            deployments = paginator.page(1)
        except EmptyPage:
            deployments = paginator.page(paginator.num_pages)
        return deployments

    def send_account_activation_email(self, from_email, to, user, base_uri):
        context = {
            'user': user,
            'base_uri': base_uri
        }
        subject = 'Activate your account'
        html_message = render_to_string('crowdusers/activate-account-mail-template.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'Crowdsourcing for Rural and Urban Areas <' + from_email + '>'
        to = to
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    def send_password_reset_email(self, from_email, to, user, base_uri, uid, token):
        context = {
            'user': user,
            'base_uri': base_uri,
            'uid': uid,
            'token': token
        }
        subject = 'Reset your account password'
        html_message = render_to_string('crowdusers/password-reset-email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'Crowdsourcing for Rural and Urban Areas <' + from_email + '>'
        to = to
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    def days_since_deployment(deployment_date):
        date_format = '%Y-%m-%d'
        current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
        formatted_deployment_date = datetime.strptime(
            dt.datetime.strptime(deployment_date, '%d.%m.%Y').strftime('%Y-%m-%d'), date_format)
        date_diff = current_date - formatted_deployment_date
        return date_diff.days
