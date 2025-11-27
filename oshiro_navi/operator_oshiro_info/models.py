# operator_oshiro_info/models.py
from django.db import models


class OshiroInfo(models.Model):
    """
    お城の基本情報テーブル（oshiro_info）。
    お城名・画像・住所・築城年などを管理する。
    """

    oshiro_name = models.CharField(
        max_length=50,
        help_text="お城名"
    )
    oshiro_images = models.ImageField(
        upload_to="oshiro_images/",
        help_text="お城の代表画像"
    )
    address = models.CharField(
        max_length=100,
        help_text="住所"
    )
    built_year = models.IntegerField(
        help_text="築城年（西暦など）"
    )
    structure = models.TextField(
        blank=True,
        help_text="お城の構造の説明"
    )
    ruins = models.TextField(
        null=True,
        blank=True,
        help_text="遺構の説明"
    )

    class Meta:
        db_table = "oshiro_info"

    def __str__(self) -> str:
        return self.oshiro_name
