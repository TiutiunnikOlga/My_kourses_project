from tkinter.constants import CASCADE

from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=350,
        unique=True,
        verbose_name="Название",
        help_text="Введите название",
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Фото",
        help_text="Прикрепите Ваше фото",
    )
    description = models.CharField(
        max_length=1000, verbose_name="Описание", help_text="Введите описание курса"
    )


class Lesson(models.Model):
    name = models.CharField(
        max_length=350,
        unique=True,
        verbose_name="Название",
        help_text="Введите название",
    )
    description = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание урока",
        on_delete=models.SET_NULL,
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Фото",
        help_text="Прикрепите фото",
    )
    link = models.CharField(
        max_length=350,
        unique=True,
        verbose_name="Ссылка на видео",
        help_text="Прикрепите ссылку на видео",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
