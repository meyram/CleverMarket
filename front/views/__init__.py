from .catalog import *
from .error import *
from .news import *
from .front import *
from .stuff import *
from .favourites import *
from django.shortcuts import render
from company.models import Company


def testView(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
    }
    return render(request, 'front/test.html', context=context)

