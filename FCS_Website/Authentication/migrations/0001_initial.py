# Generated by Django 3.2.12 on 2022-10-30 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=1024)),
                ('email', models.EmailField(max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='organization',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.user')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('image_1', models.ImageField(max_length=254, upload_to=None)),
                ('image_2', models.ImageField(max_length=254, upload_to=None)),
                ('image_3', models.ImageField(blank=True, max_length=254, upload_to=None)),
                ('image_4', models.ImageField(blank=True, max_length=254, upload_to=None)),
                ('image_5', models.ImageField(blank=True, max_length=254, upload_to=None)),
            ],
            bases=('authentication.user',),
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.user')),
                ('aadhar', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=10)),
                ('dob', models.DateField()),
            ],
            bases=('authentication.user',),
        ),
    ]