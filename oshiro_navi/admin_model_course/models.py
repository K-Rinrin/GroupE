from django.db import models

class ModelCourse(models.Model):
    """
    モデルコーステーブル（model_course）。
    コース名・距離・所要時間・コース概要・難易度・評価を管理する。
    ★スポット情報もここに統合して管理する。
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

    # --- 基本情報 ---
    model_course_name = models.CharField(max_length=30, help_text="モデルコース名")
    distance = models.FloatField(help_text="コースの距離")
    required_time = models.TimeField(help_text="コースの所要時間")
    course_overview = models.TextField(blank=True, help_text="コース概要")
    difficulty = models.CharField(max_length=20, help_text="難易度（文字列）")
    five_star_review = models.FloatField(default=0, help_text="評価（5段階などの数値）")

    # --- ▼▼▼ 追加: スポット1の情報 ▼▼▼ ---
    spot1_name = models.CharField(max_length=100, blank=True, null=True, help_text="スポット1名称")
    spot1_short = models.TextField(blank=True, null=True, help_text="スポット1短い説明")
    spot1_detail = models.TextField(blank=True, null=True, help_text="スポット1詳細")
    spot1_image = models.ImageField(upload_to='model_course_spots/', blank=True, null=True, help_text="スポット1画像")
    spot1_note = models.TextField(blank=True, null=True, help_text="スポット1補足")

    # --- ▼▼▼ 追加: スポット2の情報 ▼▼▼ ---
    spot2_name = models.CharField(max_length=100, blank=True, null=True, help_text="スポット2名称")
    spot2_short = models.TextField(blank=True, null=True, help_text="スポット2短い説明")
    spot2_detail = models.TextField(blank=True, null=True, help_text="スポット2詳細")
    spot2_image = models.ImageField(upload_to='model_course_spots/', blank=True, null=True, help_text="スポット2画像")
    spot2_note = models.TextField(blank=True, null=True, help_text="スポット2補足")

    class Meta:
        db_table = "model_course"

    def __str__(self) -> str:
        return f"ModelCourse(id={self.id}, name={self.model_course_name})"