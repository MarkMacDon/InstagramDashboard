# Generated by Django 3.1.5 on 2021-01-21 05:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210120_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.TextField(default='#hashtag', validators=[django.core.validators.RegexValidator(code='invalid_hashtags', message='Hashtag format invalid', regex='^(#\\w+\\s+)+$')]),
        ),
    ]