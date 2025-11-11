from urllib import response

from django.urls import reverse
from rest_framework import status, response
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@admin.ru')
        self.course = Course.objects.create(name='Курс разработчика', description='Лучший курс для изучения')
        self.lesson = Lesson.objects.create(name='Урок первый', link='https://www.youtube.com/12/', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-detail', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson-list')
        data = {
            'name': 'Урок 1',
            'course': self.course.pk,
            'owner': self.user.pk,
            'link': 'https://www.youtube.com/'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson-detail', args=[self.lesson.pk])
        data = {
            'name': "Первый урок",
            'link': self.lesson.link,
            'course': self.course.pk,
            'owner': self.user.pk,

        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Первый урок"
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson-detail', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "preview": None,
                    "link": self.lesson.link,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@admin.ru')
        self.course = Course.objects.create(name='Валидация', description='Основы валидации')
        self.lesson = Lesson.objects.create(name='Урок первый', link='https://www.youtube.com/12/', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=[self.course.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse('materials:course-list')
        data = {
            'name': 'Курс мастера',
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_course_update(self):
        url = reverse('materials:course-detail', args=[self.course.pk])
        data = {
            'name': 'Курс мастера приемщика',
            'description': 'Лучший в мире курс'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Курс мастера приемщика"
        )

    def test_course_delete(self):
        url = reverse('materials:course-detail', args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('materials:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "lesson_count": 1
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

