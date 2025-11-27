# admin_model_course/models.py
from django.db import models


class ModelCourse(models.Model):
    """
    モデルコーステーブル（model_course）。
    コース名・距離・所要時間・コース概要・難易度・評価を管理する。
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
        help_text="モデルコースを登録した管理者"
    )

    model_course_name = models.CharField(
        max_length=30,
        help_text="モデルコース名"
    )

    distance = models.FloatField(
        help_text="コースの距離"
    )

    required_time = models.TimeField(
        help_text="コースの所要時間"
    )

    course_overview = models.TextField(
        blank=True,
        help_text="コース概要"
    )

    difficulty = models.CharField(
        max_length=20,
        help_text="難易度（文字列）"
    )

    five_star_review = models.FloatField(
        help_text="評価（5段階などの数値）"
    )

    class Meta:
        db_table = "model_course"

    def __str__(self) -> str:
        return f"ModelCourse(id={self.id}, name={self.model_course_name})"
