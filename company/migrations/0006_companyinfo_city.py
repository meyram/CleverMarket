# Generated by Django 3.0.4 on 2020-09-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_category_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='city',
            field=models.TextField(default=''),
        ),
    ]
