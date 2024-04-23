from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(_("First-Name"), max_length=50)
    last_name = models.CharField(_("Last-Name"), max_length=50)
    identification_code = models.CharField(
        _("Identification Code"), unique=True)
    image1 = models.ImageField(_("Image1"), upload_to="user/", null=True)
    image2 = models.ImageField(_("Image2"), upload_to="user/", null=True)
    role = models.CharField(_("Role"))

    USERNAME_FIELD = "identification_code"
    REQUIRED_FIELDS = ("first_name", "last_name", "role")

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def update_login_time(self):
        self.last_login = timezone.now()
        self.save()
