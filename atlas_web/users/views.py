from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    RedirectView,
    UpdateView,
)

from atlas_web.users.forms import UserCreationForm, UserPasswordResetForm

User = get_user_model()


class UserRegisterView(CreateView):
    """ Public-facing and sends out emails on POST success --> protected /w captcha """

    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:redirect")

    # TODO: put email confirmation link in the email

    def form_valid(self, form):
        valid = super().form_valid(form)
        email, password = (
            form.cleaned_data.get("email"),
            form.cleaned_data.get("password1"),
        )
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            return valid
        # No else on purpose. We'll see what breaks so we can fix it :-) ..


class UserLoginView(LoginView):
    """ Public-facing, but does not send out emails --> not protected /w captcha """

    template_name = "users/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    template_name = "users/logged_out.html"
    next_page = reverse_lazy("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.pk) != str(kwargs.get("pk", None)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """ Password-protected, and POST success does not send email --> not protected /w captcha """

    model = User
    fields = ["email", "first_name", "last_name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Info successfully updated")
        )
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    slug_field = "pk"
    slug_url_kwarg = "pk"
    success_url = reverse_lazy("users:register")

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.pk) != str(kwargs.get("pk", None)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, _("Your account was succesfully deleted")
        )
        return super().delete(request, *args, **kwargs)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


class UserPasswordChangeView(PasswordChangeView):
    """ Password-protected, and POST success does not send email --> not protected /w captcha """

    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:redirect")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Password change success!")
        )
        return super().form_valid(form)


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "users/password_change_done.html"


class UserPasswordResetView(PasswordResetView):
    """
    Public-facing and sends out emails on POST success --> protected /w captcha
    This view sends the first email with a reset token to the user email address.
    """

    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    # TODO: dispatch? /w request.users.full_name
    # extra_email_context = {"full_name": "request.user.full_name"}
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = UserPasswordResetForm

    def form_valid(self, form):
        valid = super().form_valid(form)
        email = form.cleaned_data.get("email")
        self.request.session["password_reset_email"] = email
        return valid


class UserPasswordResetDoneView(PasswordResetDoneView):
    """ This view is shown after the form to request a reset token has been submitted """

    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """ This view is when the user clicks the password reset link to choose a new password """

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:redirect")
    post_reset_login = True

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Passsword reset success!")
        )
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


# Export the class-based views for ease of import elsewhere
user_register_view = UserRegisterView.as_view()
user_login_view = UserLoginView.as_view()
user_logout_view = UserLogoutView.as_view()
user_detail_view = UserDetailView.as_view()
user_update_view = UserUpdateView.as_view()
user_delete_view = UserDeleteView.as_view()
user_redirect_view = UserRedirectView.as_view()
user_password_change = UserPasswordChangeView.as_view()
user_password_change_done = UserPasswordChangeDoneView.as_view()
user_password_reset = UserPasswordResetView.as_view()
user_password_reset_done = UserPasswordResetDoneView.as_view()
user_password_reset_confirm = UserPasswordResetConfirmView.as_view()
user_password_reset_complete = UserPasswordResetCompleteView.as_view()
