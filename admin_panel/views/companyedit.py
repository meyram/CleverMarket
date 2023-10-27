from django.shortcuts import render, redirect, get_object_or_404
from company.helper import *
from company.models import Company, Category, CompanyCategory, news, Reviews, Services, Branches, Subscribes, CompanyFiles, File, Property, city, redactingCompanies, CompanyMessage
from admin_panel.models import Card
from django.contrib.auth.decorators import login_required
from admin_panel.decorators import *
from company_panel.models import Balance, Invoice


@login_required
@user_is_company
def forcompanyEditView(request):
    company_id = request.user.pk
    company = get_object_or_404(Company, owner=request.user)
    categori = CompanyCategory.objects.filter(company=company)
    company_fily = File.objects.filter(company_files=company.files)
    redacting_comp = redactingCompanies.objects.all()
    cities = City.objects.all()
    services = Services.objects.all()
    categories = Category.objects.all()
    parents = categories.filter(parent__isnull=False)
    try:
        category = CompanyCategory.objects.get(company=company)
    except CompanyCategory.DoesNotExist:
        category = None
    branche = Branches.objects.all()
    try:
        company_members = CompanyMembers.objects.filter(company=company)
    except CompanyMembers.DoesNotExist:
        company_members = None

    company_categories = Category.objects.filter(
        pk__in=CompanyCategory.objects.filter(company=company).values_list('category'))
    context = {
        'company': company,
        'categories': categories,
        'company_categories': company_categories,
        'company_members': company_members,
        'services': services,
        'parents': parents,
        'branches': branche,
        'cities': cities,
        'company_files': company_fily,
        'categori': categori,
        'category': category,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'info':
            name = request.POST['name']
            short_description = request.POST['short_description']
            description = request.POST['description']
            city = request.POST['city']
            phone = request.POST['phone']

            site = request.POST['site']
            worktime = request.POST['worktime']
            adress = request.POST['adress']
            r_name = "default"
            regs = City.objects.values_list('region', flat=True).filter(city_name=city)
            for reg_id in regs:
                reg = region.objects.filter(pk=reg_id)
                for r in reg:
                    r_name = r.region_name
            company_info = company.info
            company_info.name = name
            company_info.short_description = short_description
            company_info.description = description
            company_info.city = city
            company_info.region = r_name
            company_info.phone = phone
            company_info.worktime = worktime
            company_info.adress = adress
            company_info.site = site
            company_info.save()
            company.save()
            return redirect('edit')
            # return render(request, 'admin_panel/admin-company-edit.html', context=context)

        if type == 'category':
            categories_id = request.POST.getlist('categories')
            company_categories = CompanyCategory.objects.filter(company=company)
            for company_category in company_categories:
                company_category.delete()
            for category_id in categories_id:
                category = Category.objects.get(pk=category_id)
                CompanyCategory(company=company, category=category).save()


            return redirect('edit')

        if type == 'service':
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES.get('image')
            Services.objects.create(name=name, description=description, price=price, company_fk=company.pk, image=image)
            return redirect('edit')

        if type == 'branches':
            city = request.POST['city']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            worktime = request.POST['worktime']
            Branches.objects.create(city=city, address=address, phone=phone, email=email, worktime=worktime,
                                    company_fk=company.pk)
            return redirect('edit')

        if type == 'files_banner':
            files = company.files
            files.banner = request.FILES.get('banner')
            files.save()

            return redirect('edit')

        if type == 'files_logo':
            files = company.files
            files.picture = request.FILES.get('picture')
            files.save()
            return redirect('edit')

        if type == 'banner_delete':
            files = company.files
            files.banner.delete()
            files.save()
            return redirect('edit')

        if type == 'logo_delete':
            files = company.files
            files.picture.delete()
            files.save()
            return redirect('edit')

        if type == 'files_core':
            file = company.files
            files_num = File.objects.filter(company_files=file).count()
            post_file = request.FILES.get('files')
            note = request.POST['note']
            if not post_file:
                context['error_file'] = 2
                return render(request, 'admin_panel/company-edit.html', context=context)
            elif files_num == 3:
                context['error_file'] = 0
                return render(request, 'admin_panel/company-edit.html', context=context)
            else:
                File.objects.create(company_files=file, file=post_file, note=note, file_name=post_file)
                context['error_file'] = 1
                return render(request, 'admin_panel/company-edit.html', context=context)

        if type == 'delete':
            company.delete()
            return redirect('panel')
        if type == 'pass_edit':
            old_password = request.POST['old_password']
            password = request.POST['password']
            re_password = request.POST['re_password']
            user = User.objects.get(username=company.owner.username)
            if password == re_password:
                if user.check_password(old_password):
                    user.set_password(password)
                    user.save()
                    context['error'] = 'Пароль успешно изменен!'
                    return render(request, 'admin_panel/company-edit.html', context=context)
                else:
                    context['error'] = 'Старый пароль неверный!'
                    return render(request, 'admin_panel/company-edit.html', context=context)
            else:
                context['error'] = 'Пароли не совпадают!'
                return render(request, 'admin_panel/company-edit.html', context=context)
        if type == 'member-add':
            if company_members.count() == 3:
                context['errors'] = 'Превышен лимит партнёров! Максимальное количество партнёров 3'
                return render(request, 'admin_panel/company-edit.html', context=context)
            else:
                member_login = request.POST['login']
                try:
                    member_company = Company.objects.get(owner__username=member_login)
                except Company.DoesNotExist:
                    member_company = None
                if member_login == company.owner.username:
                    context['errors'] = 'Это ваш логин'
                    return render(request, 'admin_panel/company-edit.html', context=context)
                else:
                    if member_company != None and member_company.status == company.StatusChoices.ACCEPTED:
                        try:
                            CompanyMembers.objects.get(company=company, member=member_company)
                            context['errors'] = 'Эта компания уже является вашим партнёром'
                            return render(request, 'admin_panel/company-edit.html', context=context)
                        except CompanyMembers.DoesNotExist:
                            CompanyMembers.objects.create(company=company, member=member_company)
                            return redirect('edit')
                    else:
                        context['errors'] = 'Такой компании не существует'
                        return render(request, 'admin_panel/company-edit.html', context=context)
    else:
        pass

    return render(request, 'admin_panel/company-edit.html', context=context)

@login_required
@user_is_moder
def moderationCompanyView(request):
    redacting_comp = redactingCompanies.objects.all()
    context = {
           'redacting_comp': redacting_comp,
    }
    return render(request, 'admin_panel/moderation-needed-companies.html', context=context)

@login_required
@user_is_moder
def moderationEditView(request,company_id):
    redactCompany= redactingCompanies.objects.filter(company_pk=company_id)
    company = get_object_or_404(Company, pk=company_id)
    company_fily = File.objects.filter(company_files=company.files)
    categori = reCompanyCategory.objects.all()
    company_message = CompanyMessage.objects.all()
    cities = City.objects.all()
    services = Services.objects.all()
    categories = Category.objects.all()

    branche = Branches.objects.all()
    company_categories = Category.objects.filter(
        pk__in=CompanyCategory.objects.filter(company=company).values_list('category'))
    context = {
        'company': company,
        'categories': categories,
        'company_categories': company_categories,
        'services': services,
        'branches': branche,
        'cities': cities,
        'company_files': company_fily,
        'categori': categori,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'info':
            name = request.POST['name']
            short_description = request.POST['short_description']
            description = request.POST['description']
            city = request.POST['city']
            phone = request.POST['phone']
            site = request.POST['site']
            worktime = request.POST['worktime']
            adress = request.POST['adress']
            status = request.POST['status']
            r_name = "default"
            regs = City.objects.values_list('region', flat=True).filter(city_name=city)
            for reg_id in regs:
                reg = region.objects.filter(pk=reg_id)
                for r in reg:
                    r_name = r.region_name
            company_info = company.info
            company_info.name = name
            company_info.short_description = short_description
            company_info.description = description
            company_info.city = city
            company_info.region = r_name
            company_info.phone = phone
            company_info.worktime = worktime
            company_info.adress = adress
            company_info.site = site
            if status == '0':
                company.status = company.StatusChoices.ACCEPTED
            elif status == '1':
                company.status = company.StatusChoices.PENDING
            elif status == '2':
                company.status = company.StatusChoices.BANNED
            company_info.save()
            redactCompany.delete()
            company.save()
            return redirect('moder-companies')
            # return render(request, 'admin_panel/admin-company-edit.html', context=context)

        if type == 'category':
            categories_id = request.POST.getlist('categories')
            company_categories = CompanyCategory.objects.filter(company=company)
            for company_category in company_categories:
                company_category.delete()
            for category_id in categories_id:
                category = Category.objects.get(pk=category_id)
                CompanyCategory(company=company, category=category).save()
            return redirect('edit', company_id)

        if type == 'service':
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES.get('image')
            Services.objects.create(name=name, description=description, price=price, company_fk=company.pk, image=image)
            return redirect('edit', company_id)

        if type == 'branches':
            city = request.POST['city']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            worktime = request.POST['worktime']
            Branches.objects.create(city=city, address=address, phone=phone, email=email, worktime=worktime,
                                    company_fk=company.pk)
            return redirect('edit', company_id)

        if type == 'files':
            files = company.files
            files.picture = request.FILES.get('picture')
            files.banner = request.FILES.get('banner')
            files.save()
            return redirect('edit', company_id)

        if type == 'files_core':
            file = company.files
            files_num = File.objects.filter(company_files=file).count()
            post_file = request.FILES.get('files')
            note = request.POST['note']
            if not post_file:
                context['error_file'] = 2
                return render(request, 'admin_panel/moderation-edit-companies.html', context=context)
            elif files_num == 3:
                context['error_file'] = 0
                return render(request, 'admin_panel/moderation-edit-companies.html', context=context)
            else:
                File.objects.create(company_files=file, file=post_file, note=note)
                context['error_file'] = 1
                return render(request, 'admin_panel/moderation-edit-companies.html', context=context)
        if type == 'delete':
            message = request.POST['message']
            CompanyMessage.objects.create(company=company,description=message)
            redactCompany.delete()
            return redirect('moder-companies')
        if type == 'pass_edit':
            password = request.POST['password']
            re_password = request.POST['re_password']
        if password == re_password:
            user = User.objects.get(username=company.owner.username, password=old_password)
            user.set_password(password)
            user.save()
            context['error'] = 'Пароль успешно изменен!'
            return render(request, 'admin_panel/moderation-edit-companies.html', context=context)
    else:
        pass


    return render(request, 'admin_panel/moderation-edit-companies.html', context=context)
