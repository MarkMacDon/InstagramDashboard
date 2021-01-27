from celery import Celery
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'celery_example.settings'

app = Celery('celery_example',
             broker='amqp://',
             backend='rpc://',
             include=['celery_example.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()