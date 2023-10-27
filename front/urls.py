from django.urls import path
from .views import *


urlpatterns = [
    path('', FrontPageView, name='FrontPage'),
    path('catalog', catalogPageView, name='Catalog'),
    path('catalog-item/<int:company_id>', catalogItemPageView, name='Catalog-item'),

    path('contacts', contactPageView, name='contact'),

    path('default', defaultPageView, name='default'),
    path('error', errorPageView, name='error'),
    path('black-list', blacklistPageView, name='black-list'),

    path('favourites', favouritesPageView, name='favourites'),
    path('favourites-delete', remove_from_favourites, name='favourites-remove'),
    path('favourites-add', add_to_favourites, name='favourites-add'),

    path('auth-register', RegisterView, name='auth-register'),
    path('verification/<int:company_id>', verificationView, name='verification'),
    path('mailer', mailerView, name='mailer'),
    path('subscribe', SubscribeView, name='subscribe'),


    path('mobile-search', mobileSearchPageView, name='mobile-search'),

    path('news', newsPageView, name='news'),
    path('news-item/<int:news_id>', newsItemPageView, name='news-item'),

    path('about',aboutPageView, name='about'),
    path('for-clients',forClientsPageView, name='for-clients'),
    path('for-members',forMembersPageView, name='for-members'),
    path('company-register',companyRegisterView, name='companyRegister'),
    path('politics',politicsPageView, name='politics'),
    path('dogovor',dogovorPageView, name='dogovor'),

]
