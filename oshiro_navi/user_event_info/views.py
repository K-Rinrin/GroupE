import calendar
from datetime import date, timedelta
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from event_info_management.models import OperatorEvent,AdminEvent
from django.views.generic import DetailView 


class EventCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "user_event_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. URLパラメータから年月を取得（なければ現在の年月）
        year = int(self.request.GET.get('year', date.today().year))
        month = int(self.request.GET.get('month', date.today().month))

        # 2. カレンダーの生成
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        # 3. 前後の月を計算
        first_day_of_month = date(year, month, 1)
        prev_month_date = first_day_of_month - timedelta(days=1)
        next_month_date = (first_day_of_month + timedelta(days=32)).replace(day=1)

        # 4. イベントの取得
        events = AdminEvent.objects.filter(
            public_settings=True,
            start_date__year=year,
            start_date__month=month
        )

        event_dict = {}
        for event in events:
            day = event.start_date.day
            if day not in event_dict:
                event_dict[day] = []
            event_dict[day].append(event)

        # contextにデータを詰め込む
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
    """
    イベント詳細画面用のView。
    カレンダーから渡された pk (プライマリキー) を元に 1件のイベント情報を取得する。
    """
    model = AdminEvent
    template_name = "event_detail.html" # 詳細画面のHTMLファイル名
    context_object_name = "event"       # HTML内で使う変数名 {{ event.xxx }}

    def get_queryset(self):
        """
        セキュリティ設定：
        公開設定(public_settings)がTrueのイベントのみ取得可能にする。
        """
        return AdminEvent.objects.filter(public_settings=True)