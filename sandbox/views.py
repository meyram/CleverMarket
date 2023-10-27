from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def sandboxView(request):
    print(request.POST)
    if request.method == 'POST':
        form = CompanyRegisterForm(data=request.POST)
        if form.is_valid():
            return redirect('panel')
    else:
        form = CompanyRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'sandbox/index.html', context=context)
