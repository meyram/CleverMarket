from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from ..models import Card
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from ..decorators import *
from company_panel.models import Balance


@login_required
@user_is_admin
def employeesView(request):
    cards = Card.objects.filter(~Q(role=Card.RoleChoices.COMPANY_OWNER))
    context = {
        'cards': cards,
    }
    return render(request, 'admin_panel/admin-sotrud.html', context=context)


@login_required
@user_is_admin
def employeeAddView(request):
    context = {
    }
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        role = request.POST['role']
        status = request.POST['status']
        context['username'] = username
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['email'] = email
        context['role'] = role
        context['status'] = status
        if password == re_password:
            try:
                user = User.objects.get(username=username)
                context['error'] = 1
                return render(request, 'admin_panel/admin-sotrud-add.html', context=context)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                user.save()
                balance = Balance.objects.create(owner=user)
                balance.save()
                card = Card(owner=user)
                if role == '0':
                    card.role = Card.RoleChoices.MODERATOR
                else:
                    card.role = Card.RoleChoices.ADMINISTRATOR

                if status == '0':
                    card.status = Card.StatusChoices.ACTIVE
                else:
                    card.status = Card.StatusChoices.DELETED

                card.save()
                context['error'] = 0
                return render(request, 'admin_panel/admin-sotrud-add.html', context=context)
        else:
            context['error'] = 2
            return render(request, 'admin_panel/admin-sotrud-add.html', context=context)
    else:
        pass
    return render(request, 'admin_panel/admin-sotrud-add.html', context=context)


@login_required
@user_is_admin
def employeeEditView(request, employee_card_id):
    card = get_object_or_404(Card, pk=employee_card_id)
    user = card.owner
    raw_password = "XXsalamdias!XX"
    context = {
        'card': card,
        'raw_password': raw_password,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'employee-edit':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            re_password = request.POST['re_password']
            role = request.POST['role']
            status = request.POST['status']
            if password == re_password:
                if user.username != username and User.objects.filter(username='username').count():
                    context['error'] = 1
                    return render(request, 'admin_panel/admin-sotrud-edit.html', context=context)
                else:
                    user.username = username
                    if password != raw_password:
                        user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    if role == '0':
                        card.role = Card.RoleChoices.MODERATOR
                    else:
                        card.role = Card.RoleChoices.ADMINISTRATOR
                    if status == '0':
                        card.status = Card.StatusChoices.ACTIVE
                    else:
                        card.status = Card.StatusChoices.DELETED
                    card.save()
                    context['error'] = 0
                    return render(request, 'admin_panel/admin-sotrud-edit.html', context=context)
            else:
                context['error'] = 2
            return render(request, 'admin_panel/admin-sotrud-edit.html', context=context)
        else:
            pass
        if type == 'delete':
            card.delete()
            print('deleted')
            return redirect('employees')
    return render(request, 'admin_panel/admin-sotrud-edit.html', context=context)
