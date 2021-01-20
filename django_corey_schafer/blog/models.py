from django_corey_schafer import settings
from django.db import models
from django.template.defaultfilters import default
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from PIL import Image


#TODO Is the character limit inclusive of hashtags?
#TODO Set scheduled date to only allow future dates
#TODO determine the CSV format for uploading posts
#TODO add hashtags
class Post(models.Model):
    title = models.CharField(("Title"), max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='images')
    small_image = models.FileField(default='default.jpg')
    content = models.TextField(max_length=2200)
    date_added = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField(default=timezone.now)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save(**kwargs)

     
   
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk':self.pk})
