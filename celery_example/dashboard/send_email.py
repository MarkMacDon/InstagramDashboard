from celery_example.tasks import send_email_task

def send_email(delay, title, handle, content):
    send_email_task.apply_async((title, handle, content), countdown=delay)
