from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, resolve_url, redirect
from django.conf import settings
from django.contrib.auth import views as views_auth, REDIRECT_FIELD_NAME
from django.views import View
from crowdusers.forms import *
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from crowdusers.utils import *


class CustomLoginView(views_auth.LoginView):
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None

    def get_success_url(self):
        # log user in based on user role
        url = self.get_redirect_url()
        if self.request.user.is_superuser:
            return url or resolve_url(settings.SUPERUSER_LOGIN_REDIRECT_URL)
        else:
            return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class Account(View):
    def get(self, request):
        context = {
            'form': CustomUserForm()
        }
        return render(request, 'crowdusers/signup.html', context)

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.add_message(request, messages.ERROR, 'Your passwords must match')
            # do checks to verify email doesn't exist in user table
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.add_message(request, messages.ERROR,
                                     'An account with email %s ' % form.cleaned_data['email'] +
                                     ' already exist. If this is your email please login or reset your password')
            else:
                user = User.objects.create_user(email=form.cleaned_data['email'],
                                                username=form.cleaned_data['username'],
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                password=form.cleaned_data['password'], is_active=False)
                CrowdSourcingUtils.send_account_activation_email(self, settings.EMAIL_HOST_USER, user.email, user,
                                                        settings.APP_BASE_URI)
                messages.add_message(request, messages.SUCCESS,
                                     'Your account has been created. Please check your email and verify your account')
        messages.add_message(request, messages.ERROR, form.errors)
        return redirect('signup')

    def activate_user_account(request, username):
        user = User.objects.filter(username=username)
        if not user.exists():
            messages.add_message(request, messages.ERROR,
                                 "We couldn't find an account with the username '" + username + "'")
            return redirect('/accounts/login/')
        else:
            user = user.first()
            if user.is_active:
                messages.add_message(request, messages.WARNING, "Account is already activated. You can login now")
                return redirect('/accounts/login/')
            else:
                user.is_active = 'True'
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Your account has been activated successfully. You can login now")
                return redirect('/accounts/login/')

    def change_password(request):
        return render(request, 'registration/password_reset_form.html')

    def send_password_reset_email(request):
        email = request.POST.get('email', False)
        user = User.objects.filter(email=email)
        if user.count() > 0:
            user = user.first()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            CrowdSourcingUtils.send_password_reset_email(Account.send_password_reset_email, settings.EMAIL_HOST_USER,
                                                email, user, settings.APP_BASE_URI, uid, token)
            return render(request, 'registration/password_reset_done.html')
        else:
            messages.add_message(request, messages.INFO,
                                 'The email %s ' % email + ' has not been registered on our site. '
                                                           'Please check the email and try again.')
            return render(request, 'registration/password_reset_form.html')

