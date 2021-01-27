# Generated by Django 3.1.4 on 2021-01-27 08:11

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('image', models.ImageField(default='default.jpg', upload_to='images', verbose_name='Image: JPEG, GIF, or PNG')),
                ('small_image', models.FileField(default='default.jpg', upload_to='')),
                ('content', models.TextField(max_length=2200)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('scheduled_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.BooleanField(default=False)),
                ('hashtags', models.TextField(default='#hashtag', validators=[django.core.validators.RegexValidator(code='invalid_hashtags', message='Hashtag format invalid', regex='^#\\w+(?: #\\w+)*$')], verbose_name='Hashtags: must be separated by a space')),
                ('handles', models.TextField(default=django.contrib.auth.models.User, validators=[django.core.validators.RegexValidator(code='invalid_hashtags', message='Handle(s) format invalid', regex='^([a-zA-Z0-9_][a-zA-Z0-9_.])*$')], verbose_name='Handles')),
                ('permission', models.BooleanField(default=False, verbose_name='By checking this box you are giving us permission you use this content')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]