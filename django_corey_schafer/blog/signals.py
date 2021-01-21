from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_corey_schafer import settings
from .models import Post

from django.core.files.uploadedfile import SimpleUploadedFile




#! Creating Works. Updating creates a recursion error when using save 
#! and does not save a new image when it updates
#* solved Recursion error with bool 'updated'.
#TODO Get small_image to save and load from folder
#TODO Find source of duplicate data and delete old pics on post update

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
        # img = Image.open(instance.image.path)
        # img.thumbnail(output_size)
        # img.save(instance.small_image.path)
        # instance.save()
        img = Image.open(instance.image.path)
        width = img.width
        height = img.height
        top = 0
        bottom = height
        right = width
        left = 0
        if width > height:
            dif = (width - height) / 2 
            top = 0
            bottom = height
            right = width - dif
            left = dif
        elif width < height:
            dif = (height - width)/2
            top = dif
            bottom = height - dif
            height = width
            left = 0
            
        crop_rectangle = (left, top, right, bottom)
        cropped_im = img.crop(crop_rectangle)
        output_size = (350, 350)
        cropped_im.thumbnail(output_size)   
        cropped_im.save(instance.small_image.path)
        instance.save()


    Post.objects.filter(pk=instance.pk).update(updated=False)
