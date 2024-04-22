from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, identification_code, first_name, last_name, role, password, **extra_fields):
        if not identification_code:
            raise ValueError(_("The identification_code must be set"))
        user = self.model(
            identification_code=identification_code,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, identification_code, first_name, last_name, role, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(identification_code, first_name, last_name, role, password, **extra_fields)
