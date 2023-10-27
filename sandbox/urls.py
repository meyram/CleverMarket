from django.urls import path
from .views import *

urlpatterns = [
    path('', sandboxView, name='sandbox'),
]