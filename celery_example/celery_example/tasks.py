from celery.app import shared_task
from .celery import app
from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(title, handles, content, hashtags, image):
    body = f'''
    Title: \n {title} \n \n 
    Handles: \n {handles} \n \n 
    Content: \n {content} \n \n 
    Hashtags: \n {hashtags}
    '''
    email = EmailMessage(
        'Image attached',
        body,
        'mark205205@hotmail.com',
        ['markgroundupcoach@gmail.com'])
    email.attach_file(image)
    email.send()

    return None

@shared_task
def revoke_task(id):
    app.control.revoke(id)
