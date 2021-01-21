# Generated by Django 3.1.5 on 2021-01-21 05:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210120_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='handle',
            field=models.CharField(default='Enter your Instagram Handle here', max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_handle', message='Handle format invalid', regex='^ ([A-Za-z0-9._](?:(?:[A-Za-z0-9._] | (?:\\.(?!\\.))){2, 28}(?: [A-Za-z0-9._]))?)$')], verbose_name='Handles'),
        ),
    ]
