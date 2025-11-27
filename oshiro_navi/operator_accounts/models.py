# operator_accounts/models.py
from django.db import models
from django.conf import settings


class Operator(models.Model):
    """
    運営プロファイル。
    クラス図の「運営」に相当。
    アカウントと1対1で紐づく。
    """

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="operator_profile",
        help_text="運営としてのアカウント"
    )

    class Meta:
        db_table = "operator"
        verbose_name = "運営"
        verbose_name_plural = "運営"

    def __str__(self):
        return f"Operator({self.account.username})"
