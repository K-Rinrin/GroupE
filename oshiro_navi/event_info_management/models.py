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
        null=True,
        blank=True,
        help_text="イベントを主催する運営"
    )

    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        db_column="admin",
        null=True,
        blank=True,
        help_text="登録を行った管理者"
    )

    event_info = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="イベント名"
    )

    event_overview = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="イベント概要"
    )

    venue = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="開催場所"
    )

    date_and_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="開催日時"
    )

    # 0:非公開 / 1:公開 を想定
    public_settings = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="公開設定（0:非公開, 1:公開）"
    )

    class Meta:
        db_table = "event_info"

    def __str__(self) -> str:
        return f"Event(id={self.id}, name={self.event_info})"
