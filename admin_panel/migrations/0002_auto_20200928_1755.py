# Generated by Django 3.0.4 on 2020-09-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'active'), ('DELETED', 'deleted'), ('BANNED', 'banned')], default='ACTIVE', max_length=255),
        ),
    ]