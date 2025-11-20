from datetime import timedelta, timezone

from celery import shared_task

from users.models import User


@shared_task
def block_inactive_users():
    one_month = timezone.now() - timedelta(30)
    incative = User.objects.filter(last_login=one_month, is_active=True)
    inactive_count = incative.update(is_active=False)
    print(f"Заблокировано пользователей: {inactive_count}")
    return inactive_count
