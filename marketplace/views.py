from django.shortcuts import render
from django.http import HttpResponse


def error_400_view(request, exception=None):
    context = {
        'error': '400',
        'error_description': 'Неправильный запрос',
    }
    return render(request, 'front/error.html',context)



def error_403_view(request, exception=None):
    context = {
        'error_description': 'У вас нет доступа',
        'error': '403',
    }
    return render(request, 'front/error.html', context)


def error_404_view(request, exception=None):
    context = {
        'error': '404',
        'error_description': 'Страница не найдена',
    }
    return render(request, 'front/error.html', context)


def error_500_view(request, exception=None):
    context = {
        'error': '500',
        'error_description': 'С сервером что-то не так',
    }
    return render(request, 'front/error.html', context)