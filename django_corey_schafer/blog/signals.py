from PIL import Image
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_corey_schafer import settings
from .models import Post
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urlparse


#! Creating Works. Updating creates a recursion error when using save 
#! and does not save a new image when it updates
#* solved Recursion error with bool 'updated'.
#TODO Make small_image square
#TODO Get small_image to save and load from folder

@receiver(post_save, sender=Post)
def save_small_image(sender, created, instance, **kwargs):
    if created:
        print("NEW CREATED")
        basename = settings.MEDIA_ROOT + "\\images\\" + str(instance.image)
        instance.small_image = SimpleUploadedFile(basename, instance.image.read())
        output_size = (300, 300)
        instance.save()

    elif instance.updated == False:
        instance.updated = True
        print(instance.updated)
        print("UPDATED")
        basename = settings.MEDIA_ROOT + "\\images\\" + str(instance.image)
        instance.small_image = SimpleUploadedFile(basename, instance.image.read())
        a = SimpleUploadedFile(basename, instance.image.read())
        instance.save()
        Post.objects.filter(pk=instance.pk).update(small_image=a, updated=True)
        output_size = (300, 300)
        img = Image.open(instance.image.path)
        img.thumbnail(output_size)
        img.save(instance.small_image.path)
        instance.save()

    Post.objects.filter(pk=instance.pk).update(updated=False)
