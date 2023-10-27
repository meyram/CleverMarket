from django.urls import path
from .views import *

urlpatterns = [
    path('', adminPanelView, name='panel'),

    path('companies', companyView, name='companies'),
    path('company-edit/<int:company_id>', companyEditView, name='company-edit'),

    path('edit', forcompanyEditView, name='edit'),

    path('service-edit/<int:service_id>', serviceEditView, name='service-edit'),
    path('user-service-edit/<int:service_id>', serviceUserEditView, name='user-service-edit'),
    path('company-testedit/<int:company_id>', companytestEditView, name='company-testedit'),
    path('company-add', companyAddView, name='company-add'),
    path('moderation-companies', moderationCompanyView, name='moder-companies'),
    path('moderation-edit/<int:company_id>', moderationEditView, name='moder-edit'),


    path('company-category', companyCategoryView, name='company-category'),
    path('company-category-edit/<int:category_id>', companyCategoryEditView, name='company-category-edit'),
    path('category-property-edit/<int:property_id>', CategoryPropertyEditView, name='category-property-edit'),

    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),


    path('employees', employeesView, name='employees'),
    path('employee-add', employeeAddView, name='employee-add'),
    path('employee-edit/<int:employee_card_id>', employeeEditView, name='employee-edit'),

    path('balance-charge/<int:user_id>', balanceChargeView, name='balance-charge'),
    path('select-tarif/<int:company_id>', TarifView, name='tarif'),
    path('tarif-add', TarifAddView, name='tarif-add'),
    path('tarif-edit/<int:tarif_id>', TarifEditView, name='tarif-edit'),
    path('my-balance', BalanceView, name='my-balance'),

    path('takeout/company/<int:company_id>', companyTakeoutView, name='takeout-company'),

    path('news', newsView, name='admin-news'),
    path('news-edit/<int:news_id>', newsEditView, name='news-edit'),
    path('news-add', newsAddView, name='news-add'),

    path('reviews', ReviewsView, name='reviews'),
    path('reviews-user', ReviewsUserView, name='reviews-user'),
    path('review-edit/<int:Review_id>', ReviewsEditView, name='review-edit'),

    path('subscribes', SubscribesView, name='subscribes'),

    path('city', CityView, name='city'),
    path('city-edit/<int:city_id>', CityEditView, name='city-edit'),
    path('region', regionView, name='region'),
    path('region-edit/<int:region_id>', regionEditView, name='region-edit'),

    path('file-edit/<int:file_id>', fileEditView, name='file-edit'),
    path('branch-edit/<int:branch_id>', branchEditView, name='branch-edit'),

    path('user-file-edit/<int:file_id>', fileUserEditView, name='user-file-edit'),
    path('user-branch-edit/<int:branch_id>', branchUserEditView, name='user-branch-edit'),
    path('member-delete/<int:member_id>', memberDeleteView, name='member-delete'),
    path('member-user-delete/<int:member_id>', memberUserDeleteView, name='member-user-delete'),

    path('tarifes-update', CheckForExpDate, name='tarifes-update'),
]

