# Generated by Django 3.2.12 on 2022-11-01 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_delete_document'),
        ('Documents', '0002_auto_20221031_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='shared_with_doctors',
            field=models.ManyToManyField(blank=True, to='Authentication.doctor'),
        ),
        migrations.AlterField(
            model_name='document',
            name='shared_with_hospital',
            field=models.ManyToManyField(blank=True, to='Authentication.hospital'),
        ),
        migrations.AlterField(
            model_name='document',
            name='shared_with_insurance_firm',
            field=models.ManyToManyField(blank=True, to='Authentication.insurance_firm'),
        ),
        migrations.AlterField(
            model_name='document',
            name='shared_with_pharmacy',
            field=models.ManyToManyField(blank=True, to='Authentication.pharmacy'),
        ),
    ]
