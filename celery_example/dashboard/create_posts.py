from io import BytesIO

from django.core.files.base import ContentFile
from .models import Post
from django.contrib.auth.models import User
import os
from PIL import Image

#TODO Update this to reflect updated model class
def create_posts():
    users = User.objects.all()
    i = 0
    directory = r'C:\Users\mark2\Pictures\BoulderDenim'
    for pic in os.listdir(directory):

        #Iterate through users    
        if i >= len(users) - 1:
            i = 0
        else:
            i+=1   
        user = users[i]
        

        post = Post(title='Generated from python',
                    content='Content generated from python',
                    author=user)

        #Load jpegs from image directory
        folder_path = r'C:\Users\mark2\Pictures\BoulderDenim\\'
        pic_path = f'{folder_path}{pic}'
        
        #Save image
        image = Image.open(pic_path)
        thumb_io = BytesIO()
        image.save(thumb_io, image.format, quality=60)
        post.image.save(f'{post.image}', ContentFile(thumb_io.getvalue()), save=False)        
        
        post.save()
        print(post)
