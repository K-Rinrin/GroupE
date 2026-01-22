from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
 
 
class ModelCourse(models.Model):
    """
    モデルコーステーブル（親）
    コース全体の基本情報を管理する。
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
 
 
    class Meta:
        db_table = "model_course"
 
    def __str__(self) -> str:
        return f"{self.model_course_name} (ID: {self.id})"
 
 
 
 
class ModelCourseSpot(models.Model):
    """
    モデルコースのスポット情報（子）
    1つのコースに対して複数のスポットを登録できる。
    """
    # 親となるコースへの紐づけ
    model_course = models.ForeignKey(
        ModelCourse,
        on_delete=models.CASCADE,
        related_name="spots",
        help_text="紐づくモデルコース"
    )
 
   
    order = models.PositiveIntegerField(default=0, help_text="表示順序")
 
    # --- スポット詳細情報 ---
    name = models.CharField(max_length=100, blank=True, null=True, help_text="スポット名称")
    short_description = models.TextField(blank=True, null=True, help_text="スポット短い説明")
    detail = models.TextField(blank=True, null=True, help_text="スポット詳細")
    image = models.ImageField(upload_to='model_course_spots/', blank=True, null=True, help_text="スポット画像")
    note = models.TextField(blank=True, null=True, help_text="スポット補足")
 
    class Meta:
        db_table = "model_course_spot"
        ordering = ['order']
 
    def __str__(self) -> str:
        return f"{self.order}. {self.name} ({self.model_course.model_course_name})"
    



class CourseReview(models.Model):
    """
    ユーザーによる個別の評価を保存するテーブル
    """
    model_course = models.ForeignKey(
        ModelCourse, 
        on_delete=models.CASCADE, 
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="評価（1〜5）"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_review"
        # 1人のユーザーが同じコースに複数回評価できないようにする
        unique_together = ('model_course', 'user')