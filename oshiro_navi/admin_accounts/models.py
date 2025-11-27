# admin_accounts/models.py
from django.db import models
from django.conf import settings


class Admin(models.Model):
    """
    管理者プロファイル。
    クラス図の「管理者」に相当。
    アカウントと1対1で紐づき、管理するお城1〜5を持つ。
    """

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="admin_profile",
        help_text="管理者としてのアカウント"
    )

    # 管理するお城1〜5
    oshiro_management1 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="admin_slot1",
        help_text="管理するお城1"
    )
    oshiro_management2 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="admin_slot2",
        help_text="管理するお城2"
    )
    oshiro_management3 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="admin_slot3",
        help_text="管理するお城3"
    )
    oshiro_management4 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="admin_slot4",
        help_text="管理するお城4"
    )
    oshiro_management5 = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="admin_slot5",
        help_text="管理するお城5"
    )

    class Meta:
        db_table = "admin"
        verbose_name = "管理者"
        verbose_name_plural = "管理者"

    def __str__(self):
        return f"Admin({self.account.username})"
