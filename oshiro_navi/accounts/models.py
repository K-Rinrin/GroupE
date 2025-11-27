# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    """
    アカウント（ログインユーザー）。
    クラス図の「アカウント」に相当する。
      - Email → AbstractUser.email
      - ID    → AbstractUser.username を 6文字IDとして利用
      - Pass  → AbstractUser.password
      - アカウント名 → 追加フィールド account_name
    """

    # ↓ AbstractUser が持っている username を「ID（6文字）」として上書き
    username = models.CharField(
        "ID",
        max_length=6,
        unique=True,
        help_text="ログイン用ID（6文字）",
    )

    # 表示名（ニックネーム）
    account_name = models.CharField(
        max_length=30,
        blank=True,
        help_text="画面上に表示するアカウント名"
    )

    # 必要なら first_name / last_name を使わない前提で空OKにしておく
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "account"
        verbose_name = "アカウント"
        verbose_name_plural = "アカウント"

    def __str__(self) -> str:
        # ID と アカウント名を見やすく表示
        return f"{self.username} ({self.account_name})"
