from io import BytesIO
from PIL import Image


def image_resize(img):
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
    cropped_im.thumbnail(output_size, Image.ANTIALIAS)
    b = BytesIO()
    cropped_im.save(b, format='jpeg')
    final_image = Image.open(b)  
    return final_image