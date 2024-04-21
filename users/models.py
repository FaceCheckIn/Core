from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    first_name = models.CharField(_("First-Name"), max_length=50)
    last_name = models.CharField(_("Last-Name"), max_length=50)
    email = models.EmailField(_("Email"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def update_login_time(self):
        self.last_login = timezone.now()
        self.save()
