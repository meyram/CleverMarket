# Generated by Django 3.0.4 on 2020-10-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0038_auto_20201025_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='image',
            field=models.ImageField(default='company_files/pictures/Bi-group.png', upload_to='company_files/images'),
        ),
    ]
