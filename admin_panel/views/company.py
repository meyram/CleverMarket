from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from company.helper import *
from company.models import Company, Category, CompanyCategory, news, Reviews, Services, branches, Subscribes, CompanyFiles, File, Property, city, CompanyMembers
from admin_panel.models import Card
from django.contrib.auth.decorators import login_required
from admin_panel.decorators import *
from company_panel.models import Balance, Invoice   
from datetime import date,datetime, timedelta
from array import array

@login_required
@user_is_moder
def companyView(request):
    companies = Company.objects.all()
    tarif = CompanyTarif.objects.all()
    context = {
        'companies': companies,
        'tarif': tarif,
    }
    return render(request, 'admin_panel/admin-companies.html', context=context)


@login_required
@user_is_moder
def companyAddView(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        re_password = request.POST['re_password']
        context = {
            'username': username,
            'name': name,
        }
        if password == re_password:
            try:
                user = User.objects.get(username=username)
                context['error'] = 1
                return render(request, 'admin_panel/admin-company-add.html', context=context)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                balance = Balance.objects.create(owner=user)
                balance.save()
                card = Card(owner=user, role=Card.RoleChoices.COMPANY_OWNER)
                card.save()
                create_company(user, name)

                context['error'] = 0
                return render(request, 'admin_panel/admin-company-add.html', context=context)
        else:
            context['error'] = 2
            return render(request, 'admin_panel/admin-company-add.html', context=context)
    else:
        context = {
            'categories':categories,
        }
    return render(request, 'admin_panel/admin-company-add.html', context=context)


@login_required
@user_is_moder
def companyEditView(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_fily = File.objects.filter(company_files=company.files)
    cities = City.objects.all()
    services = Services.objects.all()
    categories = Category.objects.all()
    branche = Branches.objects.all()
    companies = Company.objects.all()
    try:
        company_members = CompanyMembers.objects.filter(company=company)
    except CompanyMembers.DoesNotExist:
        company_members = None
    company_categories = Category.objects.filter(
        pk__in=CompanyCategory.objects.filter(company=company).values_list('category'))
    context = {
        'company': company,
        'categories': categories,
        'company_members': company_members,
        'company_categories': company_categories,
        'services': services,
        'branches': branche,
        'cities': cities,
        'company_files': company_fily,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'info' and request.POST['email']:
            name = request.POST['name']
            short_description = request.POST['short_description']
            description = request.POST['description']
            city = request.POST['city']
            phone = request.POST['phone']
            email = request.POST['email']
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
            company_info.email = email
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
            company.save()
            return redirect('company-edit', company_id)
            #return render(request, 'admin_panel/admin-company-edit.html', context=context)

        if type == 'category':
            categories_id = request.POST.getlist('categories')
            company_categories = CompanyCategory.objects.filter(company=company)
            for company_category in company_categories:
                company_category.delete()
            for category_id in categories_id:
                category = Category.objects.get(pk=category_id)
                CompanyCategory(company=company, category=category).save()
            return redirect('company-edit',company_id)


        if type == 'service':
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES.get('image')
            Services.objects.create(name=name, description=description, price=price, company_fk=company.pk,image=image)
            return redirect('company-edit',company_id)


        if type == 'branches':
            city = request.POST['city']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            worktime = request.POST['worktime']
            Branches.objects.create(city=city, address=address, phone=phone, email=email, worktime=worktime,
                                    company_fk=company.pk)
            return redirect('company-edit',company_id)



        if type == 'files':
            files = company.files
            files.picture = request.FILES.get('picture')
            files.banner = request.FILES.get('banner')
            files.save()
            return redirect('company-edit', company_id)

        if type == 'files_core':
            file = company.files
            files_num = File.objects.filter(company_files=file).count()
            post_file = request.FILES.get('files')
            note = request.POST['note']
            if not post_file:
                context['error_file'] = 2
                return render(request, 'admin_panel/admin-company-edit.html', context=context)
            elif files_num == 3:
                context['error_file'] = 0
                return render(request, 'admin_panel/admin-company-edit.html', context=context)
            else:
                File.objects.create(company_files=file,file=post_file,note=note, file_name=post_file)
                context['error_file'] = 1
                return render(request, 'admin_panel/admin-company-edit.html', context=context)
        if type == 'delete':
            company.delete()
            return redirect('companies')
        if type == 'pass_edit':
            password = request.POST['password']
            re_password = request.POST['password']
            if password == re_password:
                user = User.objects.get(username=company.owner.username)
                user.set_password(password)
                user.save()
                context['error'] = 'Пароль успешно изменен!'
                return render(request, 'admin_panel/admin-company-edit.html', context=context)

        if type == 'member-add':
                member_login = request.POST['login']
                try:
                    member_company = Company.objects.get(owner__username=member_login)
                except Company.DoesNotExist:
                    member_company = None
                if member_login == company.owner.username:
                    context['errors'] = 'Это ваш логин'
                    return render(request, 'admin_panel/admin-company-edit.html', context=context)
                else:
                    if member_company != None and member_company.status == company.StatusChoices.ACCEPTED:
                        try:
                            CompanyMembers.objects.get(company=company,member=member_company)
                            context['errors'] = 'Эта компания уже является вашим партнёром'
                            return render(request, 'admin_panel/admin-company-edit.html', context=context)
                        except CompanyMembers.DoesNotExist:
                                CompanyMembers.objects.create(company=company, member=member_company)
                                return redirect('company-edit', company_id)
                    else:
                        context['errors'] = 'Такой компании не существует'
                        return render(request, 'admin_panel/admin-company-edit.html', context=context)

    else:
        pass

    return render(request, 'admin_panel/admin-company-edit.html', context=context)


@login_required
@user_is_moder
def companytestEditView(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    categories = Category.objects.all()
    company_categories = Category.objects.filter(
        pk__in=CompanyCategory.objects.filter(company=company).values_list('category'))
    context = {
        'company': company,
        'categories': categories,
        'company_categories': company_categories,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'info':
            name = request.POST['name']
            short_description = request.POST['short_description']
            description = request.POST['description']
            company_info = company.info
            company_info.name = name
            company_info.short_description = short_description
            company_info.description = description
            company_info.save()
            return render(request, 'front/catalog-item.html', context=context)

        if type == 'category':
            categories_id = request.POST.getlist('categories')
            company_categories = CompanyCategory.objects.filter(company=company)
            for company_category in company_categories:
                company_category.delete()
            for category_id in categories_id:
                category = Category.objects.get(pk=category_id)
                CompanyCategory(company=company, category=category).save()

        if type == 'files':
            files = company.files
            files.banner = request.FILES.get('banner', None)
            files.picture = request.FILES.get('picture', None)
            files.save()

    else:
        pass

    return render(request, 'admin_panel/test/company-edit.html', context=context)


@login_required
@user_is_moder
def companyCategoryView(request):
    categories = Category.objects.all()
    parents = categories.filter(parent__isnull=True)
    context = {
        'categories': categories,
        'parents': parents,
    }
    if request.method == 'POST':
        name = request.POST['name']
        parent_id = int(request.POST['parent_id'])
        if parent_id:
            parent = Category.objects.get(pk=parent_id)
        else:
            parent = None
        if Category.objects.filter(name=name).count():
            context['error'] = 1
        elif not name:
            context['error'] = 2
        else:
            category = Category(name=name, parent=parent)
            category.save()
            context['error'] = 0
    return render(request, 'admin_panel/admin-company-category.html', context=context)


@login_required
@user_is_moder
def companyCategoryEditView(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.all()
    parents = categories.filter(parent__isnull=True)
    properties = Property.objects.all()
    context = {
        'category': category,
        'properties': properties,
        'parents': parents,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            name = request.POST['name']
            if request.POST['parent_id']:
                parent_id = int(request.POST['parent_id'])
                if parent_id:
                    parent = Category.objects.get(pk=parent_id)
            else:
                parent = None
            if category.name != name and Category.objects.filter(name=name).count():
                context['error'] = 1
            elif not name:
                context['error'] = 2
            else:
                category.name = name
                category.parent = parent
                category.save()
                context['error'] = 0
                return redirect('company-category-edit',category_id)
            return redirect('company-category-edit', category_id)
        if type == 'property-add':
            property = request.POST['property']
            Property.objects.create(category=category,name=property)
        if type == 'delete':
            category.delete()
            return redirect('company-category')

    return render(request, 'admin_panel/admin-company-category-edit.html', context=context)


@login_required
@user_is_admin
def balanceChargeView(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    balance = user.balance
    context = {
        'user_id': user_id,
        'userr': user,
    }
    if request.method == 'POST':
        value = int(request.POST['value'])
        invoice = Invoice.objects.create(value=value, balance=balance, from_administration=True)
        invoice.save()
        invoice.update()
        redirect('balance-charge',user_id)
    return render(request, 'admin_panel/test/balance_charge.html', context=context)


@login_required
@user_is_moder
def newsView(request):
    New = News.objects.all()
    context = {
        'New': New,
    }
    return render(request, 'admin_panel/admin-news.html', context=context)


@login_required
@user_is_moder
def newsEditView(request, news_id):
    new = get_object_or_404(News, pk=news_id)
    context = {
        'new': new,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            title = request.POST['title']
            description = request.POST['description']
            text = request.POST['text']
            image = request.FILES.get('img')
            New = new
            New.title = title
            New.description = description
            New.img = image
            New.text = text
            New.save()
        if type == 'delete':
            new.delete()
            return redirect('admin-news')
    return render(request, 'admin_panel/admin-news-edit.html', context=context)


@login_required
@user_is_moder
def newsAddView(request):
    context = {
    }
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        text = request.POST['text']
        image = request.FILES.get('img')
        New = News.objects.create(title=title, description=description, text=text, img=image)
        New.title = title
        New.description = description
        New.text = text
        New.save()
        context['error'] = 0
        return render(request, 'admin_panel/admin-news-add.html', context=context)
    return render(request, 'admin_panel/admin-news-add.html', context=context)


@login_required
@user_is_moder
def ReviewsView(request, ):
    Review = Reviews.objects.all()
    companies = Company.objects.all()
    context = {
        'companies': companies,
        'Reviews': Review,
    }
    return render(request, 'admin_panel/admin-reviews.html', context=context)

@login_required
@user_is_company
def ReviewsUserView(request):
    user = request.user
    user_company = Company.objects.get(owner=user)
    try:
        reviews = Reviews.objects.filter(pk_number=user_company.pk)
    except Reviews.DoesNotExist:
        reviews = None
    Review = Reviews.objects.all()
    companies = Company.objects.all()
    context = {
        'companies': companies,
        'reviews': reviews,
    }
    return render(request, 'admin_panel/user-reviews.html', context=context)

@login_required
@user_is_moder
def SubscribesView(request, ):
    Subscribe = Subscribes.objects.all()
    companies = Company.objects.all()
    context = {
        'companies': companies,
        'Subscribes': Subscribe,
    }
    return render(request, 'admin_panel/admin-subscribes.html', context=context)


@login_required
@user_is_moder
def ReviewsEditView(request, Review_id):
    Review = get_object_or_404(Reviews, pk=Review_id)
    context = {
        'Reviews': Review,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            name = request.POST['name']
            email = request.POST['email']
            review = request.POST['review']
            status = request.POST['status']
            Review.name = name
            Review.email = email
            Review.review = review
            if status == '0':
                Review.status = Review.StatusChoices.ACTIVE
            elif status == '1':
                Review.status = Review.StatusChoices.DELETED
            else:
                Review.status = Review.StatusChoices.PENDING
            Review.save()
            return render(request, 'admin_panel/admin-reviews-edit.html', context=context)
        if type == 'delete':
            Review.delete()
            return redirect('reviews')
    return render(request, 'admin_panel/admin-reviews-edit.html', context=context)


@login_required
@user_is_moder
def TarifView(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    try:
        company_tar = CompanyTarif.objects.get(company=company)
    except CompanyTarif.DoesNotExist:
        company_tar = None
    tarifes=Tarif.objects.all()
    context = {
        'company': company,
        'tarifes': tarifes,
        'company_tar': company_tar,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            company_tarifes = CompanyTarif.objects.filter(company=company)
            tarif_id = request.POST.getlist('tarif')
            for company_tarif in company_tarifes:
                company_tarif.delete()
            for tarify in tarif_id:
                tarif=Tarif.objects.get(pk=tarify)
                CompanyTarif(company=company,tarif=tarif).save()
            return redirect('tarif', company_id)
        if type == 'delete':
            if company_tar:
                company_tar.delete()
                company.status = Company.StatusChoices.PENDING
                company.save()
                return redirect('tarif', company_id)
            else:
                context['error'] = 0
            return render(request, 'admin_panel/admin-tarif.html', context=context)

    return render(request, 'admin_panel/admin-tarif.html', context=context)

@login_required
@user_is_moder
def TarifAddView(request):
    tarifes = Tarif.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        timeleft = request.POST['timeleft']
        description = request.POST['description']
        Tarif.objects.create(name=name,price=price,timeleft=timeleft,description=description)
    context = {
        'tarifes':tarifes,
    }
    return render(request, 'admin_panel/admin-tarif-add.html', context=context)

@login_required
@user_is_moder
def TarifEditView(request,tarif_id):
    tarif = get_object_or_404(Tarif,pk=tarif_id)
    if request.method == 'POST':
        type = request.POST['form']
        if type =='edit':
            name = request.POST['name']
            price = request.POST['price']
            timeleft = request.POST['timeleft']
            description = request.POST['description']
            tarif.name = name
            tarif.price = price
            tarif.description = description
            tarif.timeleft = timeleft
            tarif.save()
            return redirect('tarif-add')
        if type == 'delete':
            tarif.delete()
            return redirect('tarif-add')
    return render(request, 'admin_panel/admin-tarif-add.html', context=context)

@login_required
@user_is_company
def BalanceView(request):
    user = request.user
    try:
        company = Company.objects.get(owner=user)
    except Company.DoesNotExist:
        company = None
    if company != None:
        try:
            company_tarif = CompanyTarif.objects.get(company=company)
        except CompanyTarif.DoesNotExist:
            company_tarif = None
    else:
        company_tarif = None

    if company != None:
        try:
            tarif = CompanyTarif.objects.get(company=company)
        except CompanyTarif.DoesNotExist:
            tarif = None
    else:
        tarif = None

    tarify = Tarif.objects.all()

    try:
        balance = user.balance
    except Balance.DoesNotExist:
        balance = Balance(owner=user)
        balance.save()

    context = {
        'balance': balance,
        'user': user,
        'company': company,
        'tarify': tarify,
        'tarif': tarif,
    }
    if request.method == 'POST':
        type = request.POST['form']
        if type=='charge':
            if(company.charged==False):
                local_time = tarif.tarif.timeleft
                d = timedelta(days=local_time)
                tarif_price = tarif.tarif.price
                if user.balance.value >= tarif_price:
                    user.balance.value -= tarif_price
                    company.exp_date = date.today() + d
                    company.charged =True
                    company.status = company.StatusChoices.ACCEPTED
                    company.save()
                    user.balance.save()
                else:
                    context['error'] = "Баланс не достаточен для списания!"
                    return render(request, 'admin_panel/admin-balance.html', context=context)
                return redirect('my-balance')
            else:
                context['error'] = "Ваш тариф еще действует!"
                return render(request, 'admin_panel/admin-balance.html', context=context)
        if type=='tarifselect':
            tarif_pk = int(request.POST['tarifselect'])
            tar = Tarif.objects.get(pk=tarif_pk)
            company_tarif.tarif = tar
            company_tarif.save()
            return redirect('my-balance')

    return render(request, 'admin_panel/admin-balance.html', context=context)


def CheckForExpDate(request):
    companies = Company.objects.all()
    company_pkshki = []
    updated_companies = []
    for company in companies:
        if company.exp_date and date.today() > company.exp_date and company.charged:
            company.status = company.StatusChoices.PENDING
            company.charged = False
            company_pkshki.append(company.pk)
            company.save()
    for pkshka in company_pkshki:
        if pkshka:
            try:
                updated_companies.append(Company.objects.get(pk=pkshka))
            except Company.DoesNotExist:
                continue
    context = {
        'companies': updated_companies,
    }
    return render(request, 'admin_panel/test/updated_tarifes.html', context=context)


@login_required
@user_is_moder
def CityView(request, ):
    cities = City.objects.all()
    regions = region.objects.all()
    if request.method =='POST':
        city_name = request.POST['name']
        region_id = int(request.POST['region_id'])
        Reg = region.objects.get(pk=region_id)
        City.objects.create(region=Reg,city_name=city_name)
    context = {
        'regions': regions,
        'cities': cities,
    }
    return render(request, 'admin_panel/admin-city.html', context=context)
@login_required
@user_is_moder
def CityEditView(request,city_id):
    city = get_object_or_404(City,pk=city_id)
    if request.method == 'POST':
        type = request.POST['form']
        if type == 'edit':
            name = request.POST['name']
            region_id = request.POST['region_id']
            regiona = region.objects.get(pk=region_id)
            city.city_name = name
            city.region = regiona
            city.save()
            return redirect('city')
        if type == 'delete':
            city.delete()
            return redirect('city')
    context = {

    }
    return render(request, 'admin_panel/admin-city-add.html', context=context)


@login_required
@user_is_moder
def regionView(request, ):
    regions = region.objects.all()
    if request.method =='POST':
        region_name = request.POST['name']
        region.objects.create(region_name=region_name)
    context = {
    'regions': regions,
    }
    return render(request, 'admin_panel/admin-region.html', context=context)
@login_required
@user_is_moder
def regionEditView(request, region_id):
    regiona = get_object_or_404(region,pk=region_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'edit':
            region_name = request.POST['name']
            regiona.region_name = region_name
            regiona.save()
            return redirect('region')
        if type == 'delete':
            regiona.delete()
            return redirect('region')
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_moder
def CategoryPropertyEditView(request, property_id):
    property = get_object_or_404(Property,pk=property_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'property_edit':
            cat_pk = int(request.POST['cat_pk'])
            name = request.POST['name']
            property_pk = request.POST['property_pk']
            properta = Property.objects.get(pk=property_pk)
            properta.name = name
            properta.save()
            return redirect('company-category-edit',cat_pk)
        if type == 'property_delete':
            cat_pk = int(request.POST['cat_pk'])
            property.delete()
            return redirect('company-category-edit',cat_pk)
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_moder
def fileEditView(request, file_id):
    files = get_object_or_404(File,pk=file_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'edit':
            files_note = request.POST['note']
            company_pk = int(request.POST['company_pk'])
            files.note = files_note
            files.save()
            return redirect('company-edit',company_pk)
        if type == 'delete':
            company_pk = int(request.POST['company_pk'])
            files.delete()
            return redirect('company-edit',company_pk)
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_moder
def branchEditView(request, branch_id):
    branch = get_object_or_404(Branches,pk=branch_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'edit':
            city = request.POST['city']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            worktime = request.POST['worktime']
            company_pk = int(request.POST['company_pk'])
            branch.city = city
            branch.address = address
            branch.phone = phone
            branch.email = email
            branch.worktime = worktime
            branch.save()
            return redirect('company-edit',company_pk)
        if type == 'delete':
            company_pk = int(request.POST['company_fk'])
            branch.delete()
            return redirect('company-edit',company_pk)
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_company
def fileUserEditView(request, file_id):
    files = get_object_or_404(File,pk=file_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'edit':
            files_note = request.POST['note']
            company_pk = int(request.POST['company_pk'])
            files.note = files_note
            files.save()
            return redirect('edit')
        if type == 'delete':
            company_pk = int(request.POST['company_pk'])
            files.delete()
            return redirect('edit')
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_company
def branchUserEditView(request, branch_id):
    branch = get_object_or_404(Branches,pk=branch_id)
    if request.method =='POST':
        type = request.POST['form']
        if type == 'edit':
            city = request.POST['city']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            worktime = request.POST['worktime']
            company_pk = int(request.POST['company_pk'])
            branch.city = city
            branch.address = address
            branch.phone = phone
            branch.email = email
            branch.worktime = worktime
            branch.save()
            return redirect('edit')
        if type == 'delete':
            company_pk = int(request.POST['company_fk'])
            branch.delete()
            return redirect('edit')
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_company
def memberDeleteView(request, member_id):
    if request.method =='POST':
        type = request.POST['form']
        if type == 'delete':
            company_pk = int(request.POST['company_pk'])
            company = get_object_or_404(Company,pk=company_pk)
            member = get_object_or_404(Company,pk=member_id)
            membership = get_object_or_404(CompanyMembers, company=company,member=member)
            membership.delete()
            return redirect('company-edit',company_pk)
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)

@login_required
@user_is_company
def memberUserDeleteView(request, member_id):
    if request.method =='POST':
        type = request.POST['form']
        if type == 'delete':
            company_pk = int(request.POST['company_pk'])
            company = get_object_or_404(Company,pk=company_pk)
            member = get_object_or_404(Company,pk=member_id)
            membership = get_object_or_404(CompanyMembers, company=company,member=member)
            membership.delete()
            return redirect('edit')
    context = {
    }
    return render(request, 'admin_panel/admin-region.html', context=context)
