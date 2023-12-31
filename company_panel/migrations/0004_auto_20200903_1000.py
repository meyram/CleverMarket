# Generated by Django 3.0.3 on 2020-09-03 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_panel', '0003_auto_20200829_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('status', models.CharField(choices=[('UNDEFINED', 'undefined'), ('AWAITING_AUTHENTICATION', 'awaiting_authentication'), ('AUTHORIZED', 'authorized'), ('COMPLETED', 'completed'), ('CANCELLED', 'cancelled'), ('DECLINED', 'declined')], default='UNDEFINED', max_length=255)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='company_panel.Balance')),
            ],
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
