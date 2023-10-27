from django.shortcuts import render, redirect, get_object_or_404
from company.helper import *
from company.models import Company, Category, CompanyCategory, news, Reviews, Services, branches, Subscribes, CompanyFiles, File, Property, city
from admin_panel.models import Card
from django.contrib.auth.decorators import login_required
from admin_panel.decorators import *
from company_panel.models import Balance, Invoice


def serviceEditView(request,service_id):
    services = get_object_or_404(Services,pk=service_id)
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            img = request.FILES.get('image')
            company_pk = int(request.POST['company_pk'])
            services.name = name
            if img is None:
                services.image = services.image
            else:
                services.image = img
            services.description = description
            services.price = price
            services.save()
        if type == 'delete':
            company_pk= int(request.POST['company_pk'])
            services.delete()
    return redirect('company-edit',company_pk)

def serviceUserEditView(request,service_id):
    services = get_object_or_404(Services,pk=service_id)
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            print('post prishel')
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            img = request.FILES.get('image')
            company_pk = int(request.POST['company_pk'])
            services.name = name
            if img is None:
                services.image = services.image
            else:
                services.image = img
            services.description = description
            services.price = price
            services.save()
        if type == 'delete':
            company_pk= int(request.POST['company_pk'])
            services.delete()
    return redirect('edit')