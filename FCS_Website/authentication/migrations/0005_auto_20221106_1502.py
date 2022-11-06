# Generated by Django 3.2.12 on 2022-11-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20221106_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='certificate_pass',
            field=models.CharField(default='AQbyfJMMnHyK2m6czBQt', max_length=20),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_type',
            field=models.CharField(choices=[('Pharmacy', 'Pharmacy'), ('Hospital', 'Hospital'), ('Insurance', 'Insurance')], default='Hospital', max_length=20),
        ),
    ]
