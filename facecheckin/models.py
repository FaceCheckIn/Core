from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        ENTER = ("enter", "Enter")
        EXIT = ("exit", "Exit")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sentiment = models.CharField(_("Sentiment"))
    status = models.CharField(_("Status"), choices=TransactionStatus.choices)
    datetime = models.DateTimeField(_("Datetime"))

    def __str__(self) -> str:
        return self.user.identification_code
