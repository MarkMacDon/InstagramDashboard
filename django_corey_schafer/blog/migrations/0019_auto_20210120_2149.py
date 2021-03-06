# Generated by Django 3.1.5 on 2021-01-21 05:49

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_post_hashtags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='handles',
            field=models.TextField(default=django.contrib.auth.models.User, validators=[django.core.validators.RegexValidator(code='invalid_hashtags', message='Hashtag format invalid', regex='^ ([A-Za-z0-9._](?:(?:[A-Za-z0-9._] | (?:\\.(?!\\.))){2, 28}(?: [A-Za-z0-9._]))?)$')], verbose_name='Handles'),
        ),
        migrations.AlterField(
            model_name='post',
            name='hashtags',
            field=models.TextField(default='#hashtag', validators=[django.core.validators.RegexValidator(code='invalid_hashtags', message='Hashtag format invalid', regex='^#\\w+(?: #\\w+)*$')], verbose_name='Hashtags: must be separated by a space'),
        ),
    ]
