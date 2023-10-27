from django import forms
from django.contrib.auth import authenticate

from django.contrib.auth.models import User



class CompanyRegisterForm(forms.Form):
    login = forms.CharField(max_length=255, required=True)
    name = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
    re_password = forms.CharField(max_length=255, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            raise forms.ValidationError("Username already exists")
        if password != re_password:
            raise forms.ValidationError("Password's must match")
        return self.cleaned_data


