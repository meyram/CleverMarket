from django.db import models
from .company import Company

class CompanyInfo(models.Model):
    company = models.OneToOneField(Company,
                                   on_delete=models.CASCADE,
                                   related_name='info',
                                   )
    name = models.CharField(max_length=255, default="")
    short_description = models.TextField(default="")
    description = models.TextField(default="")
    city = models.TextField(default="")
    region = models.TextField(default="")
    phone = models.TextField(default="")
    email = models.TextField(default="")
    site = models.TextField(default="")
    worktime = models.TextField(default="")
    adress = models.TextField(default="")
    bin = models.TextField(default="")
    search_info = models.TextField(default="")
    fake_id = models.IntegerField(default=0, null=True)
    emailclicks = models.IntegerField(default=0, null=True)
    serviceRequestclicks = models.IntegerField(default=0, null=True)
    phoneViewClicks = models.IntegerField(default=0, null=True)
    addressVievClicks = models.IntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        self.search_info = self.name + self.description + self.short_description
        self.search_info = self.search_info.lower()
        super(CompanyInfo, self).save()
