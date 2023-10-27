from django.db import models
from datetime import datetime
from django.utils import timezone
tz = timezone.get_default_timezone()

class News(models.Model):
    title = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    text = models.TextField(default="")
    img = models.ImageField(upload_to='news_filles/images',default='company_files/pictures/Bi-group.png')
    date = models.DateTimeField(
        default=datetime.now,
        null=True,
    )
