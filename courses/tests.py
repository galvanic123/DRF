from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from courses.models import Course, Lesson, Subscription
from users.models import CustomsUser


class LessonAPITestCase(APITestCase):
    """Тестирование уроков"""

    def setUp(self):
        self.user = CustomsUser.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="Дизайнер", description="Познавательный курс", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Введение",
            link_to_video="http://www.youtube.com/2",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование отображение урока"""

        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тестирование создание урока"""

        url = reverse("courses:lesson_create")
        data = {
            "title": "Практическое задание",
            "link_to_video": "http://www.youtube.com/2",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование редактирования урока"""
        url = reverse("courses:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Устное задание",
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Устное задание")

    def test_lesson_delete(self):
        """Тестирование удаление урока"""
        url = reverse("courses:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование отображение всех уроков"""
        url = reverse("courses:lesson_list")
        response = self.client.get(url)
        print(response.json())
        # data = response.json()
        # result = {
        #     "count": 1,
        #     "next": None,
        #     "previous": None,
        #     "results": [
        #         {
        #             "title": self.lesson.title,
        #             "description": self.lesson.description,
        #             "preview": None,
        #             "link_to_video": self.lesson.link_to_video,
        #             "course": 1,
        #             "owner": 1,
        #         }
        #     ],
        # }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create(email="admin@example.com")
        self.course = Course.objects.create(title="Кулинария. Выпечка.")
        self.lesson = Lesson.objects.create(
            title="Выбор муки", course=self.course, owner=self.user
        )
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        Subscription.objects.all().delete()
        url = reverse("courses:subscription_create")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all()[0].course, self.course)

    def test_subscription_delete(self):
        url = reverse("courses:subscription_create")
        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
