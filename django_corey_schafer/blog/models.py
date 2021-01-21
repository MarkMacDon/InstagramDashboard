from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# TODO determine the CSV format for uploading posts
# TODO MKV, MP4
# TODO Minimum duration: 3 seconds Maximum duration: 10 minutes Minimum dimentions: 640x640 pixels\
# TODO Who, where, when, any info, permissions
# TODO Make images all visible
# TODO Fix handles regex for multiple handles
# TODO Approved to post variable and page
# TODO posted reminder. Google calendar? other?


class Post(models.Model):
    title = models.CharField(("Title"), max_length=50)
    image = models.ImageField(default='default.jpg', verbose_name='Image: JPEG, GIF, or PNG', upload_to='images')
    small_image = models.FileField(default='default.jpg')
    content = models.TextField(max_length=2200)
    date_added = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField(default=timezone.now)
    updated = models.BooleanField(default=False)
    hashtags = models.TextField(default='#hashtag', verbose_name='Hashtags: must be separated by a space',
                                validators=[RegexValidator(
                                    regex=r'^#\w+(?: #\w+)*$',
                                    message='Hashtag format invalid',
                                    code='invalid_hashtags')]
                                    )
    handles = models.TextField(default=User, verbose_name='Handles',
                              validators=[RegexValidator(
                                  regex=r'^([a-zA-Z0-9_][a-zA-Z0-9_.])*$',
                                  message='Handle(s) format invalid',
                                  code='invalid_hashtags')]
                                  )
    permission = models.BooleanField(default=False, verbose_name='By checking this box you are giving us permission you use this content')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def getAuthorHandle(self):
        return self.author.handle
