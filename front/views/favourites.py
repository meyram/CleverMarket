from django.shortcuts import render, redirect
from company.models import Company, Category, Subscribes, News, CompanyInfo, City, region
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth

def favouritesPageView(request):
    regions = region.objects.all()
    companies = Company.objects.filter(status='ACCEPTED')
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
        'regions': regions,
        'companies': companies,
    }
    return render(request, 'front/favourites.html',context=context)

def add_to_favourites(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if not request.session.get('favourites'):
            request.session['favourites'] = list()
        else:
            request.session['favourites'] = list(request.session['favourites'])


        item_exist = next((item for item in request.session['favourites'] if item["type"] == request.POST.get('type') and item["id"] == id ), False)

        add_data = {
            'type': request.POST.get('type'),
            'id': id,
        }

        if not item_exist:
            request.session['favourites'].append(add_data)
            request.session.modified = True
    return redirect(request.POST.get('url_from'))

def remove_from_favourites(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        for item in request.session['favourites']:
            if item['id'] == id and item['type'] == request.POST.get('type'):
                item.clear()


        while {} in request.session['favourites']:
            request.session['favourites'].remove({})

        if not request.session['favourites']:
            del request.session['favourites']

        request.session.modified = True
    return redirect(request.POST.get('url_from'))