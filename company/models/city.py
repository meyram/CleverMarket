from django.db import models

class region(models.Model):
    region_name = models.CharField(max_length=50, default="")

class City(models.Model):
    region = models.ForeignKey(region,
                                    on_delete=models.CASCADE,
                                    related_name="region",
                                    )
    city_name = models.CharField(max_length=50, default="")
