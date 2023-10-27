from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
public_id = 'pk_69ca9f19c6ea45ce23b28052bec43'
api_key = '81394ed8558679117135af6c57342cb7'


@login_required
def balanceView(request):
    user = request.user
    try:
        balance = user.balance
    except Balance.DoesNotExist:
        balance = Balance(owner=user)
        balance.save()
    history = balance.payments.order_by('-date')
    for invoice in history:
        invoice.update()
    context = {
        'balance': balance,
        'history': history,
    }
    return render(request, 'company_panel/balance.html', context=context)

@login_required
def invoiceView(request):
    user = request.user
    try:
        balance = user.balance
    except Balance.DoesNotExist:
        balance = Balance(owner=user)
        balance.save()
    value = request.POST['value']
    invoice = Invoice.objects.create(value=value, balance=balance)
    invoice.save()
    data = {
        'invoice_id': invoice.id,
    }
    return JsonResponse(data=data)

