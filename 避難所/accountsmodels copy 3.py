# operator_accounts/models.py
from django.db import models


class Operator(models.Model):
    """
    運営テーブル（operator）。
    サイト運営側のアカウント情報。
    """

    # アカウントと1対1で紐づく
    account = models.OneToOneField(
        "accounts.Account",
        on_delete=models.CASCADE,
        db_column="account",
        null=True,
        blank=True,
        help_text="運営として使用するアカウント"
    )

    class Meta:
        db_table = "operator"

    def __str__(self) -> str:
        return f"Operator({self.account_id})"
