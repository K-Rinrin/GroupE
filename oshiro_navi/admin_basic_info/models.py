# admin_basic_info/models.py
from django.db import models


class BasicInfo(models.Model):
    """
    基本情報テーブル（basic_info）。
    お城ごとの詳細情報（入場料・営業時間・見どころ等）を管理する。
    """

    # お城情報（1対1）
    oshiro_info = models.OneToOneField(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_info",
        help_text="対象のお城情報"
    )

    # 入場料
    admission = models.IntegerField(
        help_text="入場料"
    )

   # 営業開始時間
    business_opening_hours = models.DateTimeField(
        help_text="営業開始時間"
    )
    # 営業終了時間
    business_closing_hours = models.DateTimeField(
        help_text="営業終了時間"
    )


    # アクセス情報
    access_info = models.TextField(
        help_text="アクセス情報"
    )

    # 見どころ画像
    highlights_img = models.ImageField(
        upload_to="highlights/",
        blank=True,
        help_text="見どころ画像"
    )

   # 見どころ説明
    highlights = models.TextField(
        blank=True,
        help_text="見どころ説明"
    )

  # 御城印画像
    gojoin_stamp = models.ImageField(
        upload_to="gojoin_stamp/",
        null=True,
        blank=True,
        help_text="御城印画像"
    )

  # 御城印説明
    gojoin = models.TextField(
        null=True,
        blank=True,
        help_text="御城印説明"
    )

    # MapField 相当。JSON でピン情報などを保存する想定。
    stamp_map = models.JSONField(
        help_text="周辺MAP情報"
    )

    class Meta:
        db_table = "basic_info"

    def __str__(self) -> str:
        return f"BasicInfo(oshiro={self.oshiro_info_id})"
