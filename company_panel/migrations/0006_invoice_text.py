# Generated by Django 3.0.3 on 2020-09-03 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_panel', '0005_auto_20200903_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
