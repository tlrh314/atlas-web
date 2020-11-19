from django.test import TestCase
from django.urls import reverse


class BaseViewTestCase(TestCase):
    """
    The templates/pages are served /w generic TemplateViews from the
    ROOT_URLCONF (config/urls.py), so they do not belong to an app.
    Therefore we test these pages from a non-app specific tests folder.
    """

    # Note that test data can be loaded from fixtures
    # These can be created /w python manage.py dumpdata,
    # and (generally) loaded /w python manage.py loaddata.
    # But the test runner will load these data for you (i.e.
    # no need to call the management command.
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        """
        Note that setUpTestData method is called once for the whole class,
        so the test data is shared between all test_ methods. This can
        speed up running the test suite, and individual test_ methods have
        transactional rollback to restore the database once the test is done.
        """
        super().setUpTestData()

    def setUp(self):
        """
        Note that the setUp method is called every time before the test_ method runs.
        """
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

    def test_url_to_privacy_view_in_base_cookie_notice_in_base_template(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            '"href": "/privacy/"',
            status_code=200,
        )

    def test_about(self):
        url = reverse("about")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/about.html")
        self.assertContains(
            response,
            "We can change what sits on the about page in the content block.",
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
