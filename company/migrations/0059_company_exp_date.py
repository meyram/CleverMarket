# Generated by Django 3.0.4 on 2020-10-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0058_tarif_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='exp_date',
            field=models.DateField(null=True),
        ),
    ]
