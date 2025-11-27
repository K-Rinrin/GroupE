# user_accounts/models.py
from django.db import models


class User(models.Model):
    """
    利用者テーブル（user）。
    1アカウント = 1利用者 になるように、Account と OneToOne で紐づける。
    Django側では account_id というカラム名になる。
    """

    # アカウント（一対一・これが主キー）
    account = models.OneToOneField(
        "accounts.Account",
        on_delete=models.CASCADE,
        primary_key=True,        # Userテーブルの主キーにする → 自動idは作られない
        help_text="紐づくアカウント（1アカウント = 1利用者）"
    )

    # プロフィール画像（ファイル名やパス）
    profile_image = models.CharField(
        max_length=20,
        null=True,
        help_text="プロフィール画像（ファイル名 or パス）"
    )

    # 自己紹介文
    user_about = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="自己紹介文"
    )

    class Meta:
        db_table = "user"

    def __str__(self) -> str:
        return f"User({self.account_id})"


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
        help_text="口コミを投稿した日時"
    )

    class Meta:
        db_table = "user_review"

    def __str__(self) -> str:
        return f"Review(id={self.id}, user={self.user_id})"
