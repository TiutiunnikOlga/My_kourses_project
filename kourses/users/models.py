import json
from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=100, verbose_name="Город", help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Прикрепите Ваше фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def ready(self):
        from django_celery_beat.models import IntervalSchedule, PeriodicTask

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=24, period=IntervalSchedule.HOURS
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name="Block users",
            task="users.tasks.block_inactive_users",
            args=json.dumps(["arg1", "arg2"]),
            kwargs=json.dumps({"be_careful": True}),
            expires=datetime.utcnow() + timedelta(seconds=30),
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOISES = [
        ("cash", "наличные"),
        ("transfer", "перевод"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOISES, verbose_name="Сумма оплат"
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return f"Оплата {self.amount} от {self.user} за {self.course or self.lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscribe(models.Model):
    user = (
        models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            verbose_name="Пользователь",
        ),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Подписка на курс",
    )

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки"
