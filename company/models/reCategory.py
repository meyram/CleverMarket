from django.db import models
from .company import Company
from .category import Category

class reCompanyCategory(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="re_categories",
                                )
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="re_companies",
                                 )