from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationLoginTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

        response_post = self.client.post(reverse("register"), {
            "username": "testuser",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertEqual(response_post.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_view(self):
        User.objects.create_user(username="testuser", password="ComplexPass123")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")

        response_post = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "ComplexPass123"
        })
        self.assertEqual(response_post.status_code, 302)
