from celery import Celery

import celery
print (celery.__file__)

app = Celery('django_corey_schafer',
             broker='amqp://',
             backend='rpc://',
             include=['django_corey_schafer.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()