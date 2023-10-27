from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from .models import Card
from django.http import Http404
from company.models import Company, VerificationCodes

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        try:
            card = request.user.card
        except Card.DoesNotExist:
            card = Card(owner=request.user)
            card.save()
        if (
                card.status == Card.StatusChoices.ACTIVE and
                card.role == Card.RoleChoices.ADMINISTRATOR
        ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_moder(function):
    def wrap(request, *args, **kwargs):
        try:
            card = request.user.card
        except Card.DoesNotExist:
            card = Card(owner=request.user)
            card.save()
        if (
                card.status == Card.StatusChoices.ACTIVE and
                (
                        card.role == Card.RoleChoices.MODERATOR or
                        card.role == Card.RoleChoices.ADMINISTRATOR
                )
        ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_company(function):
    def wrap(request, *args, **kwargs):
        try:
            card = request.user.card
        except Card.DoesNotExist:
            card = Card(owner=request.user)
            card.save()
        if (
                card.status == Card.StatusChoices.ACTIVE and
                (
                        card.role == Card.RoleChoices.MODERATOR or
                        card.role == Card.RoleChoices.ADMINISTRATOR or
                        card.role == Card.RoleChoices.COMPANY_OWNER
                )
        ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def company_is_active(function):
    def wrap(request,company_id, *args, **kwargs):

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            company = None
        if ( company != None and company.status == Company.StatusChoices.ACCEPTED ):
            return function(request,company_id, *args, **kwargs)
        else:
            raise Http404

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def isVerification_valid(function):
    def wrap(request, company_id, *args, **kwargs):
        company = get_object_or_404(Company,pk=company_id)
        try:
            verification = VerificationCodes.objects.get(company=company)
        except VerificationCodes.DoesNotExist:
            verification = None
        if (verification != None ):
            return function(request, company_id, *args, **kwargs)
        else:
            raise Http404

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap