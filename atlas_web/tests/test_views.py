from django.test import TestCase
from django.urls import reverse


class BaseViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_home(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/home.html")
        self.assertContains(
            response,
            "Use this document as a way to quick start any new project.",
            status_code=200,
        )

    def test_about(self):
        url = reverse("about")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/about.html")
        self.assertContains(
            response,
            "Use this document as a way to quick start any new project.",
            status_code=200,
        )

    def test_privacy(self):
        url = reverse("privacy")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/privacy.html")
        self.assertContains(
            response,
            "<h2>Data Collection and Processing</h2>",
            status_code=200,
        )
        self.assertContains(
            response,
            "<h2>Data Transmission</h2>",
            status_code=200,
        )

    def test_imprint(self):
        url = reverse("imprint")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://www.mps.mpg.de/imprint")
