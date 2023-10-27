from django.db import models
from datetime import datetime


class Reviews(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'active'
        DELETED = 'DELETED', 'deleted'
        PENDING = 'PENDING', 'pending'

    name = models.CharField(max_length=50, default="")
    pk_number = models.IntegerField(default="")
    email  = models.TextField(default="")
    review = models.TextField(default="")
    status = models.CharField(max_length=255,
                              choices=StatusChoices.choices,
                              default=StatusChoices.PENDING
                              )
    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
    )