# Generated by Django 3.1.4 on 2021-01-27 08:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')),
                ('handle', models.CharField(default='Enter your Instagram Handle here', max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_handle', message='Handle format invalid', regex='^([a-zA-Z0-9_][a-zA-Z0-9_.])*$')], verbose_name='Handles')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
