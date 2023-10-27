from django.db import models

class Branches(models.Model):

    company_fk = models.IntegerField(default=1)
    city = models.TextField(default="")
    address = models.TextField(default="")
    phone = models.TextField(default="")
    email = models.TextField(default="")
    worktime = models.TextField(default="")

class reBranches(models.Model):
    company_fk = models.IntegerField(default=1)
    city = models.TextField(default="")
    address = models.TextField(default="")
    phone = models.TextField(default="")
    email = models.TextField(default="")
    worktime = models.TextField(default="")

