from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_panel.decorators import *
from company.models import Company, CompanyInfo
from company_panel.models import Invoice
from django.contrib.auth.models import User

@login_required
@user_is_company
def adminPanelView(request):
    history = Invoice.objects.all().order_by('-date')
    user_history = Invoice.objects.filter(balance__owner= request.user)
    company_infos = CompanyInfo.objects.all()
    company_number = Company.objects.all().count()
    invoices_sum = 0

    for hi in history:
        invoices_sum += hi.value
    invoices_value = int(invoices_sum)
    emailclicks = 0
    addressVievClicks = 0
    serviceRequestclicks = 0
    phoneViewClicks = 0
    for company_info in company_infos:
        emailclicks += company_info.emailclicks
        addressVievClicks += company_info.addressVievClicks
        serviceRequestclicks += company_info.serviceRequestclicks
        phoneViewClicks += company_info.phoneViewClicks
    print(user_history)
    context = {
        'history': history,
        'user_history': user_history,
        'serviceRequestclicks': serviceRequestclicks,
        'addressVievClicks': addressVievClicks,
        'emailclicks': emailclicks,
        'phoneViewClicks': phoneViewClicks,
        'company_number': company_number,
        'invoices_sum': invoices_value,
    }
    return render(request, 'admin_panel/index.html', context=context)
