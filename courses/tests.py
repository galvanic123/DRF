from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from courses.models import Course, Lesson, Subscription
from users.models import CustomsUser


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create(email='admin@example.com')
        self.course = Course.objects.create(title='Кулинария. Выпечка.')
        self.lesson = Lesson.objects.create(title='Выбор муки', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        url = reverse('courses:course-list')
        data = {
            'title': 'Кулинария. Тушение.'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('courses:course-detail', args=(self.course.pk,))
        data = {
            'title': 'Кулинария. Тушение.'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Кулинария. Тушение.'
        )

    def test_course_delete(self):
        url = reverse('courses:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('courses:course_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create(email='admin@example.com')
        self.course = Course.objects.create(title='Кулинария. Выпечка.')
        self.lesson = Lesson.objects.create(title='Выбор муки', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('courses:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('courses:lesson_create')
        data = {
            'title': 'Тушение овощей',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('courses:lesson_update', args=(self.lesson.pk,))
        data = {
            'title': 'Тушение мяса',
            'course': self.course.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        print(response.json())

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Тушение мяса'
        )

    def test_lesson_delete(self):
        url = reverse('courses:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('courses:lesson_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create(email='admin@example.com')
        self.course = Course.objects.create(title='Кулинария. Выпечка.')
        self.lesson = Lesson.objects.create(title='Выбор муки', course=self.course, owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        Subscription.objects.all().delete()
        url = reverse('courses:subscription_create')
        data = {
            'course': self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all()[0].course, self.course
        )

    def test_subscription_delete(self):
        url = reverse('courses:subscription_create')
        response = self.client.post(url, {'course': self.course.pk})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.count(), 0
        )