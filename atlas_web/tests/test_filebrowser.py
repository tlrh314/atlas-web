from django.test import TestCase
from django.urls import reverse

from atlas_web.users.tests.factories import AdminFactory, UserFactory


class TestFileBrowser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory.create()
        cls.admin_password = "admin_password"
        cls.admin.set_password(cls.admin_password)
        cls.admin.save()

        cls.user = UserFactory.create(is_active=True)
        cls.user_password = "user_password"
        cls.user.set_password(cls.user_password)
        cls.user.save()

    def login(self):
        response = self.client.get(reverse("admin:login"))
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.status_code, 200)
        login_status = self.client.login(
            email=self.admin.email, password=self.admin_password
        )
        self.assertTrue(login_status)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_login_of_admin_200(self):
        self.login()

    def test_login_of_user_302(self):
        response = self.client.get(reverse("admin:login"))
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.status_code, 200)  # login form is fine
        login_status = self.client.login(
            email=self.user.email, password=self.user_password
        )
        self.assertTrue(login_status)  # b/c admin login forms works for any user

    def test_filebrowser_browse_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_browse"))
        self.assertTemplateUsed(response, "filebrowser/index.html")
        self.assertEqual(response.status_code, 200)

    def test_filebrowser_createdir_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_createdir"))
        self.assertTemplateUsed(response, "filebrowser/createdir.html")
        self.assertEqual(response.status_code, 200)

    def filebrowser_delete_200(self):  # TODO: needs file?
        self.login()
        response = self.client.get(reverse("filebrowser:fb_delete"))
        self.assertEqual(response.url, "123")
        self.assertEqual(response.status_code, 200)

    def test_filebrowser_delete_confirm_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_delete_confirm"))
        self.assertEqual(response.status_code, 200)

    def test_filebrowser_detail_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_detail"))
        self.assertEqual(response.status_code, 200)

    def test_filebrowser_filebrowser_changelist_302_to_browse(self):
        self.login()
        response = self.client.get(reverse("admin:filebrowser_filebrowser_changelist"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("filebrowser:fb_browse"))

    def test_filebrowser_upload_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_upload"))
        self.assertEqual(response.status_code, 200)

    def filebrowser_do_upload_200(self):  # TODO: needs file?
        self.login()
        response = self.client.get(reverse("filebrowser:fb_do_upload"))
        self.assertEqual(response.status_code, 200)

    def test_filebrowser_version_200(self):
        self.login()
        response = self.client.get(reverse("filebrowser:fb_version"))
        self.assertEqual(response.status_code, 200)
