from django.shortcuts import render
from company.models import Company


def defaultPageView(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
    }
    return render(request, 'front/default.html',context=context)

def errorPageView(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
    }
    return render(request, 'front/error.html',context=context)
