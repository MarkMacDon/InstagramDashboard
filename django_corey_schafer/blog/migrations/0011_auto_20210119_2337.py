# Generated by Django 3.1.5 on 2021-01-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210119_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='small_image',
            field=models.FileField(upload_to='small_images'),
        ),
    ]
