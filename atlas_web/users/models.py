from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from atlas_web.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for atlas-web."""

    # Basic information
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    first_name = models.CharField(_("First Name"), max_length=42)
    last_name = models.CharField(_("Last Name"), max_length=42)

    # Permissions
    is_active = models.BooleanField(
        _("Active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("Staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    # is_superuser inherited from PermissionsMixin
    is_validated = models.BooleanField(
        _("Has the User been Validated?"), blank=False, default=False
    )

    # Time stamps, and logging of who changed user info
    last_updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="has_changed_accounts",
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # email login rather than arbitrary username
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        name = self.get_full_name()
        if len(name) < 2:
            return self.email
        else:
            return name

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        full_name = "{0} {1}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def send_email(
        self,
        subject,
        text_content,
        html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        **kwargs
    ):
        """Sends an email to this User. Caution, from_email must contain domain
        name in production!"""

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[self.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
