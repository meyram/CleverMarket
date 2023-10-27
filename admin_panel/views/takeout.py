from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from company.models import Company

@login_required
def companyTakeoutView(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    context = {
        'company': company,
    }
    return render(request, 'admin_panel/company-takeout.html', context=context)
