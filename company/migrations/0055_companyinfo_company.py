# Generated by Django 3.0.4 on 2020-10-30 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0054_remove_companyinfo_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='company',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='info', to='company.Company'),
            preserve_default=False,
        ),
    ]
