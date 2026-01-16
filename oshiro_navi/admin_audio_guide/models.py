# admin_audio_guide/models.py
from django.db import models


class AudioGuide(models.Model):
    """
    音声ガイドテーブル（audio_guide）。
    お城の音声ガイド用タイトル・説明・QRコードなどを管理する。
    """

    oshiro_info = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_info",
        help_text="対象のお城情報"
    )

    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        db_column="admin",
        help_text="登録した管理者"
    )

    title = models.CharField(
        max_length=20,
        help_text="音声ガイドのタイトル"
    )

    guide_explanation = models.TextField(
        blank=True,
        help_text="ガイド内容の説明"
    )


    class Meta:
        db_table = "audio_guide"

    def __str__(self) -> str:
        return f"AudioGuide(id={self.id}, title={self.title})"
