from django.test import TestCase
from django.urls import resolve, reverse


class BaseUrlTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_home(self):
        url = reverse("home")
        self.assertEqual(url, "/")
        resolver = resolve(url)
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "home")

    def test_about(self):
        url = reverse("about")
        self.assertEqual(url, "/about/")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "about")

    def test_privacy(self):
        url = reverse("privacy")
        self.assertEqual(url, "/privacy/")

    def test_imprint(self):
        url = reverse("imprint")
        self.assertEqual(url, "/imprint/")
