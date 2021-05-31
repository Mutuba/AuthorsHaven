"""
Celery email sending implementation
"""
from __future__ import absolute_import
from django.conf import settings
import os

from celery import Celery, shared_task
from django.core.mail import EmailMessage

# set the default Django settings module for the 'celery' program.
os.environ["DJANGO_SETTINGS_MODULE"] = "authors.settings"

app = Celery("authors")

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = "UTC"


print("Registering debug task...")


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

@shared_task
def task(data_to_queue):
    """Gets payload from the user and sends it to mail"""
    mail = EmailMessage(
        subject=data_to_queue["subject"],
        body=data_to_queue["message"],
        to=data_to_queue["to"],
        from_email=data_to_queue["from_email"],
    )
    mail.content_subtype = "html"
    mail.send()


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(
    run_every=(crontab(hour="*", minute="*", day_of_week="*")), ignore_result=True
)
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    date_now = now.strftime("%d-%m-%Y %H:%M:%S")
    result = 2 + 2
    logger.info("Task finished: result = %i" % result)


@periodic_task(
    run_every=(crontab(hour="*", minute="*", day_of_week="*")), ignore_result=True
)
def add():
    logger.info("Start  Add Task")
    result = 50 + 150

    logger.info("Task finished: result = %i" % result)
    return result
