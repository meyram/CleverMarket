from django.db import models


class Services(models.Model):
    company_fk = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    price = models.TextField(default="")
    image = models.ImageField(upload_to='company_files/images', default='company_files/pictures/Bi-group.png')

class reServices(models.Model):
    company_fk = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    price = models.TextField(default="")
    image = models.ImageField(upload_to='company_files/images', default='company_files/pictures/Bi-group.png')