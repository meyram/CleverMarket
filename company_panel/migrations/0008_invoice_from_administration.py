# Generated by Django 3.0.3 on 2020-09-08 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_panel', '0007_invoice_charged'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='from_administration',
            field=models.BooleanField(default=False),
        ),
    ]