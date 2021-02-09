from celery import shared_task
from django.core.cache import cache

from .models import User


@shared_task
def cache_user_count():
    cache.set("total_users", User.objects.count())
