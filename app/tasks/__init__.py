from celery import Celery
from app.tasks.cleanup import check_and_notify_inactive_sellers

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def run_check_inactive_sellers():
    check_and_notify_inactive_sellers()
