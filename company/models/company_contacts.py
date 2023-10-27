from django.db import models
from .company import Company
from django.core.validators import RegexValidator


class CompanyContacts(models.Model):
    company = models.OneToOneField(Company,
                                   on_delete=models.CASCADE,
                                   related_name='contacts',
                                   )


class PhoneNumber(models.Model):
    company_contacts = models.ForeignKey(CompanyContacts,
                                         on_delete=models.CASCADE,
                                         related_name='phones',
                                         )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    )
    note = models.CharField(max_length=255, blank=True)


class Email(models.Model):
    company_contacts = models.ForeignKey(CompanyContacts,
                                         on_delete=models.CASCADE,
                                         related_name='emails',
                                         )
    email = models.EmailField()
    note = models.CharField(max_length=255, blank=True)


class WebSite(models.Model):
    company_contacts = models.ForeignKey(CompanyContacts,
                                         on_delete=models.CASCADE,
                                         related_name='websites',
                                         )
    url = models.URLField()
    note = models.CharField(max_length=255, blank=True)


class Address(models.Model):
    company_contacts = models.ForeignKey(CompanyContacts,
                                         on_delete=models.CASCADE,
                                         related_name='addresses',
                                         )
    address = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
