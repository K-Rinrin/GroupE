import calendar
from datetime import date, timedelta
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from event_info_management.models import OperatorEvent, AdminEvent

from datetime import date, timedelta, datetime

class EventCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "user_event_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        year = int(self.request.GET.get('year', date.today().year))
        month = int(self.request.GET.get('month', date.today().month))

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        # 表示月の範囲（開始日と終了日）を取得
        first_day = date(year, month, 1)
        # 次の月の1日の前日が今月の末日
        if month == 12:
            last_day = date(year, month, 31)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        # 1. 期間が今月にかかっているイベントをすべて取得
        # (開始日が今月末以前) かつ (終了日が今月初日以降)
        admin_events = AdminEvent.objects.filter(
            public_settings=True,
            start_date__lte=last_day,
            end_date__gte=first_day
        )
        operator_events = OperatorEvent.objects.filter(
            public_settings=True,
            start_date__lte=last_day,
            end_date__gte=first_day
        )

        event_dict = {}

        # 共通の処理用関数
        def add_events_to_dict(events, e_type):
            for event in events:
                event.event_type = e_type
                
                # イベントの期間中、今月に含まれる日をすべてループ
                curr_date = max(event.start_date, first_day)
                end_limit = min(event.end_date, last_day)
                
                while curr_date <= end_limit:
                    d = curr_date.day
                    # テンプレート判定用に開始/終了フラグを持たせる
                    # ※ これによりCSSで線を繋げられるようになります
                    event_copy = event # 同一インスタンスに属性をつけると上書きされるため注意
                    event_dict.setdefault(d, []).append(event)
                    curr_date += timedelta(days=1)

        add_events_to_dict(admin_events, 'admin')
        add_events_to_dict(operator_events, 'operator')

        # 前後の月計算
        prev_month_date = first_day - timedelta(days=1)
        next_month_date = last_day + timedelta(days=1)

        context.update({
            'month_days': month_days,
            'event_dict': event_dict,
            'year': year,
            'month': month,
            'prev_year': prev_month_date.year,
            'prev_month': prev_month_date.month,
            'next_year': next_month_date.year,
            'next_month': next_month_date.month,
        })
        return context
class EventDetailView(LoginRequiredMixin, DetailView):
    template_name = "user_event_detail.html"
    context_object_name = "event"

    def get_object(self):
        # URLから event_type と pk を取得してモデルを切り替える
        event_type = self.kwargs.get('event_type')
        pk = self.kwargs.get('pk')
        
        if event_type == 'admin':
            return get_object_or_404(AdminEvent, pk=pk, public_settings=True)
        else:
            return get_object_or_404(OperatorEvent, pk=pk, public_settings=True)