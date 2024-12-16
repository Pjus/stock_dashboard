from celery import shared_task
from .utils import update_all_stocks


@shared_task
def periodic_update_stocks():
    update_all_stocks()
