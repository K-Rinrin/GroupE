# admin_oshiro_stamp/models.py
from django.db import models


class OshiroStampInfo(models.Model):
    """
    お城スタンプ情報テーブル（oshiro_stamp_info）。
    スタンプ画像やスタンプ名などのマスタ情報。
    """

    oshiro_info = models.OneToOneField(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_info",
        null=True,
        blank=True,
        help_text="対象のお城情報（1対1）"
    )

    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        db_column="admin",
        null=True,
        blank=True,
        help_text="登録した管理者"
    )

    oshiro_stamp_image = models.ImageField(
        upload_to="oshiro_stamp_images/",
        null=True,
        blank=True,
        help_text="お城スタンプ画像"
    )

    stamp_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="スタンプ名"
    )

    class Meta:
        db_table = "oshiro_stamp_info"

    def __str__(self) -> str:
        return f"OshiroStampInfo(id={self.id}, name={self.stamp_name})"


class OshiroStamp(models.Model):
    """
    お城スタンプテーブル（oshiro_stamp）。
    利用者が集めたスタンプ数や取得日を管理する。
    """

    # テーブル定義書では PK ○ が付いているので primary_key=True
    oshiro_stamp_info = models.OneToOneField(
        "admin_oshiro_stamp.OshiroStampInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_stamp_info",
        primary_key=True,
        help_text="対象のお城スタンプ情報（主キー）"
    )

    oshiro_stamp = models.IntegerField(
        null=True,
        blank=True,
        help_text="お城スタンプ数"
    )

    date = models.DateField(
        null=True,
        blank=True,
        help_text="スタンプ取得日"
    )

    user = models.ForeignKey(
        "user_accounts.User",
        on_delete=models.CASCADE,
        db_column="user",
        null=True,
        blank=True,
        help_text="スタンプを持っている利用者"
    )

    class Meta:
        db_table = "oshiro_stamp"

    def __str__(self) -> str:
        return f"OshiroStamp(info={self.oshiro_stamp_info_id}, user={self.user_id})"
