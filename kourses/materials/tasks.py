from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_mail_on_update(email):
    send_mail(
        "Курс обновлен",
        "Вышло обновление курса, на который Вы подписаны",
        EMAIL_HOST_USER,
        [email],
    )
