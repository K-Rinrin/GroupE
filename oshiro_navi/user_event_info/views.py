import calendar
from datetime import date, timedelta
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from event_info_management.models import OperatorEvent, AdminEvent

class EventCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "user_event_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        year = int(self.request.GET.get('year', date.today().year))
        month = int(self.request.GET.get('month', date.today().month))

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        first_day_of_month = date(year, month, 1)
        prev_month_date = first_day_of_month - timedelta(days=1)
        next_month_date = (first_day_of_month + timedelta(days=32)).replace(day=1)

        # 1. 両方のモデルからイベントを取得する
        admin_events = AdminEvent.objects.filter(
            public_settings=True,
            start_date__year=year,
            start_date__month=month
        )
        operator_events = OperatorEvent.objects.filter(
            public_settings=True,
            start_date__year=year,
            start_date__month=month
        )

        # 2. 辞書にまとめる（どちらのイベントか判別できるように属性を追加）
        event_dict = {}

        # 管理者イベントの処理
        for event in admin_events:
            event.event_type = 'admin' # テンプレートでURLを分けるために使う
            day = event.start_date.day
            event_dict.setdefault(day, []).append(event)

        # 運営イベントの処理
        for event in operator_events:
            event.event_type = 'operator' # テンプレートでURLを分けるために使う
            day = event.start_date.day
            event_dict.setdefault(day, []).append(event)

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