# Generated by Django 3.1.5 on 2021-01-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210120_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='small_image',
            field=models.FileField(default='default.jpg', upload_to=''),
        ),
    ]