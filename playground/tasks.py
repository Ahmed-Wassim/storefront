from celery import shared_task


@shared_task
def notify_customers(message):
    print("")
