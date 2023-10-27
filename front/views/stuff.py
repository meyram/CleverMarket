from django.shortcuts import render,redirect
from company.models import Company, Category, Subscribes,  News, CompanyInfo, region,VerificationCodes
from admin_panel.models import Card
from company.helper import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from admin_panel.decorators import *
from django.core.mail import send_mail
from company_panel.models import Balance, Invoice
import random

def blacklistPageView(request):
    regions = region.objects.all()
    companies = Company.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
        'regions': regions,
        'companies': companies,
    }
    return render(request, 'front/black-list.html',context=context)


def mobileSearchPageView(request):
    regions = region.objects.all()
    filteredcategories = Category.objects.filter(parent__isnull=True)
    companycities = CompanyInfo.objects.values_list('city', flat=True).distinct()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'anon'
    context = {
        'username': username,
        'filteredcategories': filteredcategories,
        'companycities': companycities,
        'regions': regions,
    }
    return render(request, 'front/mobile-search.html',context=context)


def RegisterView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/auth-register.html', context=context)

@isVerification_valid
def verificationView(request,company_id):
    regions = region.objects.all()
    context = {
        'regions': regions,
        "companypk" : company_id,
    }
    verifications = VerificationCodes.objects.all()
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
        company = None
    if request.method == 'POST':
        code = request.POST['code']
        try:
            verification = VerificationCodes.objects.get(code=code)
            if company != None:
                email = verification.email
                company.info.email = email
                company.info.save()
                verification.delete()
                return redirect('panel')
            else:
                context['error'] = 0
                return render(request, 'front/verification.html', context=context)
        except VerificationCodes.DoesNotExist:
            context['error'] = 1
            return render(request, 'front/verification.html', context=context)

    return render(request, 'front/verification.html', context=context)

def mailerView(request):
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'consult':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            text = request.POST['text']
            comp_id = request.POST['compid']
            company = Company.objects.get(pk=comp_id)
            existing_clicks = company.info.emailclicks
            existing_clicks += 1
            company.info.emailclicks = existing_clicks
            company.info.save()
            company_email = request.POST['companyemail']
            send_mail('Заявка с сайта Topbuild',
                      'Имя отправителя: ' + name + '\n' +
                      'Телефон: ' + phone + '\n' +
                      'Email: ' + email + '\n' +
                      text
                      ,
                      'info@topbuild.kz',
                      [company_email],
                      fail_silently=False,
                      )
            return redirect('Catalog-item', comp_id)
        if type == 'service-call':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            text = request.POST['text']
            comp_id = request.POST['compid']
            service = request.POST['service']
            company = Company.objects.get(pk=comp_id)
            existing_clicks = company.info.serviceRequestclicks
            existing_clicks += 1
            company.info.serviceRequestclicks = existing_clicks
            company.info.save()
            company_email = request.POST['companyemail']
            send_mail('Заявка с сайта Topbuild',
                      'Имя отправителя: ' + name + '\n' +
                      'Телефон: ' + phone + '\n' +
                      'Email: ' + email + '\n' +
                      'Услуга: ' + service + '\n' +
                      text
                      ,
                      'info@topbuild.kz',
                      [company_email],
                      fail_silently=False,
                      )
            return redirect('Catalog-item', comp_id)
        if type == 'call_request':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            text = request.POST['text']
            send_mail('Заявка на звонок',
                      'Имя отправителя: ' + name + '\n' +
                      'Телефон: ' + phone + '\n' +
                      'Email: ' + email + '\n' +
                      text
                      ,
                      'info@topbuild.kz',
                      ['dias2001@inbox.ru'],
                      fail_silently=False,
                      )
            return redirect('FrontPage')
        if type == 'send_review':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            rating = request.POST['rating']
            text = request.POST['text']
            send_mail('Отзыв',
                      'Имя отправителя: ' + name + '\n' +
                      'Телефон: ' + phone + '\n' +
                      'Email: ' + email + '\n' +
                      'Оценка: ' + rating + '\n' +
                      text
                      ,
                      'info@topbuild.kz',
                      ['dias2001@inbox.ru'],
                      fail_silently=False,
                      )
            return redirect('FrontPage')

    return redirect('Catalog')

def SubscribeView(request):
    if request.method == 'POST':
        email = request.POST['email']
        Subscribes.objects.create(email=email)

    return HttpResponseRedirect('./')


def aboutPageView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/about.html', context=context)

def forClientsPageView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/for-clients.html', context=context)

def forMembersPageView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/for-members.html', context=context)

def politicsPageView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/politics.html', context=context)
def dogovorPageView(request):
    regions = region.objects.all()
    context = {
        'regions': regions,
     }
    return render(request, 'front/dogovor.html', context=context)


def companyRegisterView(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        re_password = request.POST['re_password']
        email = request.POST['email']
        context = {
            'username': username,
            'name': name,
        }
        if password == re_password:
            try:
                user = User.objects.get(username=username)
                context['error'] = 1
                return render(request, 'front/auth-register.html', context=context)
            except User.DoesNotExist:
                try:
                    company = CompanyInfo.objects.get(email=email)
                    context['error'] = 3
                    return render(request, 'front/auth-register.html', context=context)
                except CompanyInfo.DoesNotExist:
                    generated_code = random.randint(1000000, 9999999)
                    try:
                        verification = VerificationCodes.objects.get(email=email)
                        context['error'] = 4
                        return render(request, 'front/auth-register.html', context=context)
                    except VerificationCodes.DoesNotExist:
                        verification = None
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                        balance = Balance.objects.create(owner=user)
                        balance.save()
                        card = Card(owner=user, role=Card.RoleChoices.COMPANY_OWNER)
                        card.save()
                        create_company(user, name)
                        company = Company.objects.get(owner=user)
                        VerificationCodes.objects.create(company=company,code=generated_code, email=email)
                        send_mail('Подтверждение Email',
                                  'Ваш код верификации: ' + str(
                                      generated_code) + '\n' + 'Ссылка для верификации: ' + "http://topbuild.beget.tech/verification/" + str(company.pk),
                                  'info@topbuild.kz',
                                  [email],
                                  fail_silently=True,
                                  )
                        return redirect('verification', company.pk)


        else:
            context['error'] = 2
            return render(request, 'front/auth-register.html', context=context)
    else:
        context = {
        }
    return render(request, 'front/auth-register.html', context=context)
