# Generated by Django 3.0.4 on 2020-10-31 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0060_auto_20201031_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=1)),
            ],
        ),
    ]
