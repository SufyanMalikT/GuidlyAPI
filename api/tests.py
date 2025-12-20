from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from api.models import Student, Program, Application, University

class ApplicationTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="password123",
            role="student"
        )
        self.student = Student.objects.create(user=self.user, full_name="Student One")
        university = University.objects.create(name="University One",country='England',city='London')
        self.program = Program.objects.create(university=university,name="MBA", degree_level="master", duration_years=2, tuition_fee=20000)
        self.client.login(username="student1", password="password123")

    def test_create_application(self):
        url = reverse('application-list')
        data = {
            "program": self.program.id,
            "notes": "My application notes"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().student, self.student)
