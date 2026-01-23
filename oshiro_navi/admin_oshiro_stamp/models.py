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
        help_text="対象のお城情報（1対1）"
    )

    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        db_column="admin",
        help_text="登録した管理者"
    )

    oshiro_stamp_image = models.ImageField(
        upload_to="oshiro_stamp_images/",
        help_text="お城スタンプ画像"
    )

    stamp_name = models.CharField(
        max_length=20,
        help_text="スタンプ名"
    )

    class Meta:
        db_table = "oshiro_stamp_info"

    def __str__(self) -> str:
        return f"OshiroStampInfo(id={self.id}, name={self.stamp_name})"




class OshiroStamp(models.Model):
    oshiro_stamp_info = models.ForeignKey(
        "admin_oshiro_stamp.OshiroStampInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_stamp_info",
        help_text="対象のお城スタンプ情報"
    )

    date = models.DateField(
        auto_now_add=True,
        help_text="スタンプ取得日"
    )

    user = models.ForeignKey(
        "user_accounts.User",
        on_delete=models.CASCADE,
        db_column="user",
        help_text="スタンプを持っている利用者"
    )

    class Meta:
        db_table = "oshiro_stamp"
        # 「同じユーザーが同じスタンプを2個以上持てない」という制限はここでかける
        unique_together = ('user', 'oshiro_stamp_info')

    def __str__(self) -> str:
        return f"OshiroStamp(info={self.oshiro_stamp_info_id}, user={self.user_id})"
