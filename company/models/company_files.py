from django.db import models
from .company import Company


class CompanyFiles(models.Model):
    company = models.OneToOneField(Company,
                                   on_delete=models.CASCADE,
                                   related_name='files',
                                   )
    picture = models.ImageField(upload_to='company_files/pictures', blank=True)
    banner = models.ImageField(upload_to='company_files/banners', blank=True)


def make_upload_path(instance, filename):
    return u'company_files/files%s' % filename.encode('utf8')


class File(models.Model):
    company_files = models.ForeignKey(CompanyFiles,
                                          on_delete=models.CASCADE,
                                      related_name='files',
                                      )
    file_name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=make_upload_path,null=True,blank=True)
    note = models.CharField(max_length=255, blank=True)

class Image(models.Model):
    company_files = models.ForeignKey(CompanyFiles,
                                      on_delete=models.CASCADE,
                                      related_name='images',
                                      )
    image = models.ImageField(upload_to='company_files/images')
