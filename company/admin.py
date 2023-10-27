from django.contrib import admin

from .models import *


admin.site.register(Company)
admin.site.register(CompanyMembers)

admin.site.register(CompanyInfo)
admin.site.register(reCompanyInfo)

admin.site.register(CompanyContacts)
admin.site.register(PhoneNumber)
admin.site.register(Email)
admin.site.register(WebSite)
admin.site.register(Address)

admin.site.register(CompanyFiles)
admin.site.register(File)
admin.site.register(Image)

admin.site.register(Category)

admin.site.register(News)
admin.site.register(Property)
admin.site.register(Reviews)

admin.site.register(Services)
admin.site.register(Branches)
admin.site.register(Tarif)
admin.site.register(CompanyTarif)
admin.site.register(CompanyCategory)
admin.site.register(City)
admin.site.register(Subscribes)
admin.site.register(region)

admin.site.register(redactingCompanies)
admin.site.register(CompanyMessage)
admin.site.register(reCompanyFiles)
admin.site.register(reFile)
admin.site.register(reBranches)
admin.site.register(reServices)
admin.site.register(reCompanyCategory)
admin.site.register(VerificationCodes)
