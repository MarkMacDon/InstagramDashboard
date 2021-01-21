from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    handle = models.CharField(max_length=30, default='Enter your Instagram Handle here', verbose_name='Handles',
                              validators=[RegexValidator(
                                  regex=r'^([a-zA-Z0-9_][a-zA-Z0-9_.])*$',
                                  message='Handle format invalid',
                                  code='invalid_handle')]
                                  )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        #*Image resize using PIL. There are other options
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        