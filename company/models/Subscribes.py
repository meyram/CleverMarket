from django.db import models
from datetime import datetime

class Subscribes(models.Model):
    email = models.EmailField(default="")
    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
    )