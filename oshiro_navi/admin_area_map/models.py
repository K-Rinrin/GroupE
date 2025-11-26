# admin_area_map/models.py
from django.db import models


class AreaMapInfo(models.Model):
    """
    周辺MAP情報テーブル（area_map_info）。
    MAP上の1つのアイコン（トイレ・駐車場など）の情報を持つ。
    """

    basic_info = models.ForeignKey(
        "admin_basic_info.BasicInfo",
        on_delete=models.CASCADE,
        db_column="basic_info",
        help_text="紐づく基本情報（どのお城のMAPか）"
    )

    icon_name = models.CharField(
        max_length=20,
        help_text="アイコン名（例：トイレ・駐車場）"
    )

    icon_image = models.ImageField(
        upload_to="area_map_icons/",
        help_text="アイコンの画像"
    )

    latitude = models.FloatField(
        help_text="緯度"
    )
    longitude = models.FloatField(
        help_text="経度"
    )

    class Meta:
        db_table = "area_map_info"

    def __str__(self) -> str:
        return f"AreaMapInfo(id={self.id})"
