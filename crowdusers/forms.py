from django.forms import ModelForm
from .models import *
from django import forms


class DeploymentForm(ModelForm):
    class Meta:
        model = Deployment
        exclude = ['created_date', 'user']


class DeploymentImagesForm(ModelForm):
    class Meta:
        model = DeploymentImages
        fields = ('file',)


class CustomUserForm(ModelForm):
    confirm_password = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['autocomplete'] = 'off'

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
                'required': 'required',
            })

    class Meta:
        model = CustomUser
        fields = ['email', 'display_name', 'password']
        labels = {'display_name': 'Display Name'}