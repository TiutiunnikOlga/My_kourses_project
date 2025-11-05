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
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Прикрепите Ваше фото",
    )
    description = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name="Описание",
        help_text="Введите описание курса",
    )


class Lesson(models.Model):
    name = models.CharField(
        max_length=350,
        unique=True,
        verbose_name="Название",
        help_text="Введите название",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Фото",
        help_text="Прикрепите фото",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        help_text="Введите название курса",
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
