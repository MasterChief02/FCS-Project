# Generated by Django 3.2.12 on 2022-11-04 21:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('mobile_number', models.CharField(max_length=10)),
                ('verification_document', models.FileField(max_length=256, upload_to='Data/Verification', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('is_verified', models.BooleanField(default=False)),
                ('certificate_file', models.FileField(blank=True, max_length=256, upload_to='Data/Authentication', validators=[django.core.validators.FileExtensionValidator(['p12'])])),
                ('certificate_pass', models.CharField(default='FUm6MP9WVqKZVxgMMAcV', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('custom_user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.custom_user')),
                ('profile_picture', models.ImageField(max_length=254, upload_to='Data/Profile_Picture')),
                ('license_number', models.CharField(max_length=10)),
            ],
            bases=('authentication.custom_user',),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('custom_user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.custom_user')),
                ('description', models.CharField(max_length=500)),
                ('organization_type', models.CharField(choices=[('Pharmacy', 'Pharmacy'), ('Hospital', 'Hospital'), ('Insurance', 'Insurance')], default='Hospital', max_length=20)),
                ('location_address', models.CharField(max_length=50)),
                ('location_district', models.CharField(max_length=50)),
                ('location_state', models.CharField(max_length=50)),
                ('location_country', models.CharField(max_length=50)),
                ('location_pin_code', models.CharField(max_length=50)),
            ],
            bases=('authentication.custom_user',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('custom_user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.custom_user')),
                ('dob', models.DateField()),
                ('profile_picture', models.ImageField(max_length=254, upload_to='Data/Profile_Picture')),
            ],
            bases=('authentication.custom_user',),
        ),
        migrations.CreateModel(
            name='OrganizationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=254, upload_to='Data/Profile_Picture')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='authentication.organization')),
            ],
        ),
    ]
