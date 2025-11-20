from datetime import timedelta, timezone

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def block_inactive_users():
    one_month = timezone.now() - timedelta(30)
    incative = User.objects.filter(last_login=one_month, is_active=True)
    inactive_count = incative.update(is_active=False)
    print(f"Заблокировано пользователей: {inactive_count}")
    return inactive_count


def send_mail_on_update(email):
    send_mail(
        "Курс обновлен",
        "Вышло обновление курса, на который Вы подписаны",
        EMAIL_HOST_USER,
        [email],
    )
