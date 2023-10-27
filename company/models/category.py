from django.db import models
from .company import Company


class Category(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'active'
        DELETED = 'DELETED', 'deleted'

    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL,
                               related_name="childs",
                               )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255,
                              choices=StatusChoices.choices,
                              default=StatusChoices.ACTIVE
                              )

    def __str__(self):
        if self.parent:
            return str(self.parent) + '-' + self.name
        else:
            return self.name


class Property(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="properties",
                                 )
    name = models.CharField(max_length=255)



class CompanyCategory(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="categories",
                                )
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="companies",
                                 )
