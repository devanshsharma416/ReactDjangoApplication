# Generated by Django 3.2.7 on 2021-09-28 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
