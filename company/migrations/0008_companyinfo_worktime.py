# Generated by Django 3.0.4 on 2020-09-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20200923_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='worktime',
            field=models.TextField(default=''),
        ),
    ]
