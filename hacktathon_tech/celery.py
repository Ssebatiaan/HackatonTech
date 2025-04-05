from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab



# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hacktathon_tech.settings')

app = Celery('csjv')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(packages=settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    #'envio_correo': {
    #    'task': 'alerta.tasks.enviar_reporte_email_alerta',
    #    'schedule': crontab(hour='*', minute='*', day_of_week='*'),
    #    'args': (),
    #}
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    

@app.task(bind=True)
def debug_task2(self):
    print('Request: {0!r}'.format(self.request))