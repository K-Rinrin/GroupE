# user_accounts/models.py
from django.db import models
from django.conf import settings


class User(models.Model):
    """
    利用者（一般ユーザー）のプロフィール。
    クラス図の「利用者」に相当。
    Account(アカウント) と 1対1 で紐づく。
    """

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profile",
        help_text="紐づくアカウント（1アカウント = 1利用者）"
    )

    # プロフィール画像
    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True,
        help_text="プロフィール画像"
    )

    # 自己紹介
    user_about = models.TextField(
        null=True,
        blank=True,
        help_text="自己紹介文"
    )

    class Meta:
        db_table = "user"
        verbose_name = "利用者"
        verbose_name_plural = "利用者"

    def __str__(self):
        return f"User({self.account.username})"


class UserReview(models.Model):
    """
    口コミテーブル（user_review）。
    利用者が投稿するレビュー情報。
    """

    # 口コミを書いた利用者
    user = models.ForeignKey(
        "user_accounts.User",
        on_delete=models.CASCADE,
        db_column="user",
        help_text="口コミ投稿者（利用者）"
    )

    oshiro_info = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_info",
        help_text="口コミしたお城"
    )

    review_title = models.CharField(
        max_length=20,
        help_text="口コミタイトル"
    )

    review_comments = models.CharField(
        max_length=50,
        blank=True,
        help_text="口コミコメント"
    )

    review_image = models.ImageField(
        upload_to="review_images/",
        null=True,
        help_text="口コミに添付された画像"
    )

    five_star_review = models.FloatField(
        help_text="評価（数値・5段階など）"
    )

    post_date_time = models.DateTimeField(
        auto_now_add=True, #日時を自動追加
        help_text="口コミを投稿した日時"
    )

    class Meta:
        db_table = "user_review"

    def __str__(self) -> str:
        return f"Review(id={self.id}, user={self.user_id})"
