# Generated by Django 3.0.4 on 2020-09-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_auto_20200924_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='date',
            field=models.CharField(max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
