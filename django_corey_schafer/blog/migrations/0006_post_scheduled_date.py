# Generated by Django 3.1.5 on 2021-01-20 01:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210119_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='scheduled_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
