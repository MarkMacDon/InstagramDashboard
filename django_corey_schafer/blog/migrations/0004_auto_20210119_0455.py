# Generated by Django 3.1.5 on 2021-01-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210119_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='post',
            name='small_image',
            field=models.ImageField(default='default.jpg', editable=False, upload_to='profile_pics'),
        ),
    ]
