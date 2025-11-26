# admin_accounts/models.py
from django.db import models


class Admin(models.Model):
    """
    管理者テーブル（admin）。
    アカウントと1対1で紐づき、担当するお城を最大5件まで持つ。
    """

    # アカウント（主キー＆FK）
    account = models.OneToOneField(
        "accounts.Account",
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="account",
        help_text="管理者に対応するアカウント（主キー）"
    )

    # 管理するお城1〜5（Oshiro_info FK）
    oshiro_management1 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_manegement1",
        null=True,
        blank=True,
        related_name="admin_slot1",
        help_text="管理するお城1"
    )
    oshiro_management2 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_manegement2",
        null=True,
        blank=True,
        related_name="admin_slot2",
        help_text="管理するお城2"
    )
    oshiro_management3 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_manegement3",
        null=True,
        blank=True,
        related_name="admin_slot3",
        help_text="管理するお城3"
    )
    oshiro_management4 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_manegement4",
        null=True,
        blank=True,
        related_name="admin_slot4",
        help_text="管理するお城4"
    )
    oshiro_management5 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_manegement5",
        null=True,
        blank=True,
        related_name="admin_slot5",
        help_text="管理するお城5"
    )

    class Meta:
        db_table = "admin"

    def __str__(self) -> str:
        return f"Admin({self.account_id})"
