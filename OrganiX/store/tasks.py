from celery import shared_task
from store.models.products import Batch
from datetime import datetime
import pytz
from django.utils import timezone

utc = pytz.UTC
now = timezone.now()


@shared_task
def my_scheduled_task():
    return "Task is running every 2m hehe"


@shared_task
def add(x, y):
    return x + y


@shared_task
def exp_date_check():
    avail_batch = Batch.objects.filter(status=True)
    if avail_batch:
        for _ in avail_batch:
            if (
                (_.expiry_date.year < now.year)
                or (_.expiry_date.year == now.year and _.expiry_date.month < now.month)
                or (
                    _.expiry_date.year == now.year
                    and _.expiry_date.month == now.month
                    and _.expiry_date.day <= now.day
                )
            ):
                Batch.objects.filter(id=_.id).update(status=False)
    return 1
