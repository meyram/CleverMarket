# Generated by Django 3.0.4 on 2020-11-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0064_auto_20201105_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
