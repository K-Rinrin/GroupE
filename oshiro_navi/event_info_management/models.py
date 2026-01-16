
from django.db import models

class EventBase(models.Model):
    """共通項目をまとめる（テーブルは作られない）"""
    event_info = models.CharField(max_length=30, help_text="イベント名")
    event_overview = models.CharField(max_length=100, blank=True, help_text="イベント概要")
    venue = models.CharField(max_length=100, help_text="開催場所")
    
    start_date = models.DateField(help_text="開始日")
    end_date = models.DateField(help_text="終了日")
    start_time = models.TimeField(help_text="開始時間")
    end_time = models.TimeField(help_text="終了時間")
    
    public_settings = models.BooleanField(default=False, help_text="公開設定")

    class Meta:
        abstract = True

class OperatorEvent(EventBase):
    """オペレーター用：絶対にoperatorが必要（adminは持たない）"""
    operator = models.ForeignKey(
        "operator_accounts.Operator",
        on_delete=models.CASCADE,
        related_name="operator_events",
        db_column="operator"
    )

    class Meta:
        db_table = "operator_event_info"

class AdminEvent(EventBase):
    """アドミン用：絶対にadminが必要（operatorは持たない）"""
    admin = models.ForeignKey(
        "admin_accounts.Admin",
        on_delete=models.CASCADE,
        related_name="admin_events",
        db_column="admin"
    )

    class Meta:
        db_table = "admin_event_info"