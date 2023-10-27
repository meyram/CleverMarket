from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings
from django.urls import path


def response_error_handler(request, exception=None):
    print('Hello')
    return HttpResponse('Error handler content', status=403)


handler403 = response_error_handler
