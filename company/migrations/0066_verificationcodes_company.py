# Generated by Django 3.0.4 on 2020-11-05 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0065_file_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationcodes',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='VerificatingCompany', to='company.Company'),
        ),
    ]
