from django.db import models
from .company import Company
from datetime import datetime
from django.utils import timezone
tz = timezone.get_default_timezone()

class redactingCompanies(models.Model):
    company_pk = models.IntegerField(default=1)
    name = models.CharField(max_length=255, default="")
    date = models.DateTimeField(
        default=datetime.now,
        null=True,
    )