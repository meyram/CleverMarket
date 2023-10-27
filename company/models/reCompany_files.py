from django.db import models
from .company import Company


class reCompanyFiles(models.Model):
    company = models.OneToOneField(Company,
                                   on_delete=models.CASCADE,
                                   related_name='re_files',
                                   )
    picture = models.ImageField(upload_to='company_files/pictures', blank=True)
    banner = models.ImageField(upload_to='company_files/banners', blank=True)

class reFile(models.Model):
    company_files = models.ForeignKey(reCompanyFiles,
                                          on_delete=models.CASCADE,
                                      related_name='re_files',
                                      )
    file = models.FileField(upload_to='company_files/files',null=True)
    note = models.CharField(max_length=255, blank=True)


class reImage(models.Model):
    company_files = models.ForeignKey(reCompanyFiles,
                                      on_delete=models.CASCADE,
                                      related_name='re_images',
                                      )
    image = models.ImageField(upload_to='company_files/images')
