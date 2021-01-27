from celery.app import shared_task
from .celery import app
from celery import shared_task
from django.core.mail import send_mail


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@shared_task
def send_email_task(title, handles, content):
    body = title + handles + content
    send_mail('Celery Task Worked',
              body,
              'mark205205@hotmail.com',
              ['markgroundupcoach@gmail.com'])
    return None
