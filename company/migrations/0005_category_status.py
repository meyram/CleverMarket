from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20200815_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'active'), ('DELETED', 'deleted')], default='ACTIVE', max_length=255),
        ),
    ]
