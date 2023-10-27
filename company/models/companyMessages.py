from django.db import models
from .company import Company


class CompanyMessage(models.Model):
    company = models.ForeignKey(Company,
                                   on_delete=models.CASCADE,
                                   related_name='message',
                                   )
    description = models.TextField(default="")

