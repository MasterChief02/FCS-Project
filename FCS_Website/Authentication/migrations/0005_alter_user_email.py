# Generated by Django 4.1 on 2022-10-31 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "authentication",
            "0004_pending_doctor_pending_organization_pending_patient_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
