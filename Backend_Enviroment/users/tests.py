from django.contrib.auth.models import User
from django.test import TestCase

LOGIN_URL = "/api/auth/login/"
PASSWORD = "Str0ngPass!99"


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "ankit", email="aandu@gmail.com", password=PASSWORD
        )

    def login(self, username, password=PASSWORD):
        return self.client.post(
            LOGIN_URL,
            {"username": username, "password": password},
            content_type="application/json",
        )

    def test_login_with_username(self):
        res = self.login("ankit")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.json())

    def test_login_with_email(self):
        res = self.login("aandu@gmail.com")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.json())

    def test_login_with_email_is_case_insensitive_and_trimmed(self):
        res = self.login("  AAnDu@Gmail.com  ")
        self.assertEqual(res.status_code, 200)

    def test_wrong_password_is_rejected(self):
        self.assertEqual(self.login("aandu@gmail.com", "wrong").status_code, 401)

    def test_unknown_email_is_rejected(self):
        self.assertEqual(self.login("nobody@example.com").status_code, 401)

    def test_ambiguous_email_does_not_log_anyone_in(self):
        # Legacy rows can share an email; registration now blocks new ones.
        User.objects.create_user("second", email="aandu@gmail.com", password=PASSWORD)
        self.assertEqual(self.login("aandu@gmail.com").status_code, 401)

    def test_missing_fields_are_rejected(self):
        res = self.client.post(LOGIN_URL, {}, content_type="application/json")
        self.assertEqual(res.status_code, 400)


class RegisterTests(TestCase):
    URL = "/api/auth/register/"

    def register(self, **overrides):
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": PASSWORD,
        }
        payload.update(overrides)
        return self.client.post(self.URL, payload, content_type="application/json")

    def test_registered_user_can_log_in_with_either_identifier(self):
        self.assertEqual(self.register().status_code, 201)

        for identifier in ("newuser", "new@example.com"):
            res = self.client.post(
                LOGIN_URL,
                {"username": identifier, "password": PASSWORD},
                content_type="application/json",
            )
            self.assertEqual(res.status_code, 200, identifier)

    def test_weak_password_is_rejected_with_a_reason(self):
        res = self.register(password="123")
        self.assertEqual(res.status_code, 400)
        self.assertTrue(res.json()["error"])

    def test_duplicate_email_is_rejected(self):
        self.register()
        res = self.register(username="other")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "Email already registered")

    def test_invalid_email_is_rejected(self):
        self.assertEqual(self.register(email="not-an-email").status_code, 400)
