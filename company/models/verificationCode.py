from django.db import models
from .company import Company

class VerificationCodes(models.Model):
    company = models.ForeignKey(Company,
                                null=True,
                                on_delete=models.CASCADE,
                                related_name = "VerificatingCompany"
                                )
    code = models.IntegerField(default=1)
    email = models.CharField(max_length=50, default="")