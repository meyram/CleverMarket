from django.shortcuts import render,redirect
from company.models import Company, Category, Subscribes, News, CompanyInfo, City, region
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth

def FrontPageView(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    New = News.objects.order_by('-pk')
    regions = region.objects.all()
    cities = City.objects.all()
    filteredcategories = Category.objects.filter(parent__isnull=True)
    companycities = CompanyInfo.objects.values_list('city',flat=True).distinct()
    categories = Category.objects.all()
    companies = Company.objects.filter(status='ACCEPTED')
    context = {
        'username': username,
        'companies': companies,
        'categories': categories,
        'filteredcategories': filteredcategories,
        'companycities': companycities,
        'cities': cities,
        'regions': regions,
        'News': New,
    }
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'subz':
            email = request.POST['email']
            if email:
                try:
                    Subscribes.objects.get(email=email)
                    response = JsonResponse({
                        "error": 1
                    })
                    return response
                except Subscribes.DoesNotExist:
                    Subscribes.objects.create(email=email)
                    response = JsonResponse({"success":"Ura"})
                    response.status_code = 200
                    return response
            else:
                response = JsonResponse({"error": 2})
                return response

    return render(request, 'front/index.html',context=context)


def contactPageView(request):
    regions = region.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
        'regions': regions,
    }
    return render(request, 'front/contact.html',context=context)
