# accounts/models.py
from django.db import models


class Account(models.Model):
    """
    ログイン用アカウント。
    他テーブル（利用者・管理者・運営）から参照される“親”テーブル。
    """

    # メールアドレス（40文字まで）
    email = models.CharField(
        max_length=40,
        help_text="アカウントに紐づくメールアドレス"
    )

    # アカウントID（主キー・6文字）
    # テーブル定義書：ID / id / CharField(6) / PK, FK, NN, 自動採番
    id = models.CharField(
        max_length=6,
        primary_key=True,
        help_text="アカウントID（主キー）。他テーブルからも参照される"
    )

    # パスワード（ハッシュ値を想定・60文字）
    # 物理名は pass なので db_column で対応
    password = models.CharField(
        max_length=60,
        db_column="pass",
        help_text="パスワード（ハッシュ値など）"
    )

    # 表示用アカウント名（30文字）
    account_name = models.CharField(
        max_length=30,
        help_text="画面上に表示するアカウント名"
    )

    class Meta:
        db_table = "account"

    def __str__(self) -> str:
        return f"{self.id} - {self.account_name}"
