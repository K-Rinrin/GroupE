# event_info_management/models.py
from django.db import models


class EventInfo(models.Model):
    """
    イベント情報テーブル（event_info）。
    お城で開催されるイベントの概要を管理する。
    """

    operoter = models.ForeignKey(
        "operator_accounts.Operator",
        on_delete=models.CASCADE,
        db_column="operoter",
        blank=True,
        help_text="イベントを主催する運営"
    )

    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        db_column="admin",
        blank=True,
        help_text="登録を行った管理者"
    )

    event_info = models.CharField(
        max_length=30,
        help_text="イベント名"
    )

    event_overview = models.CharField(
        max_length=100,
        blank=True,
        help_text="イベント概要"
    )

    venue = models.CharField(
        max_length=100,
        help_text="開催場所"
    )

    # 開始日
    start_date = models.DateTimeField(
        help_text="イベントの開始日（日時）"
    )

    # 終了日
    end_date = models.DateTimeField(
        help_text="イベントの終了日（日時）"
    )

    # 開始時間
    start_time = models.DateTimeField(
        help_text="イベントの開始時間（日時）"
    )

    # 終了時間
    end_time = models.DateTimeField(
        help_text="イベントの終了時間（日時）"
    )

    # 0:非公開 / 1:公開 を想定
    public_settings = models.BooleanField(
        default=False,
        blank=True,
        help_text="公開設定（0:非公開, 1:公開）"
    )

    class Meta:
        db_table = "event_info"

    def __str__(self) -> str:
        return f"Event(id={self.id}, name={self.event_info})"
