# Generated by Django 3.0.4 on 2020-11-05 11:40

import company.models.company_files
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0063_auto_20201105_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=company.models.company_files.make_upload_path),
        ),
    ]
