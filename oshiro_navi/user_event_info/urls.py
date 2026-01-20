from django.urls import path
from .views import * # すべてのクラスを直接読み込んでいる

app_name = "user_event_info"

urlpatterns = [
    # views. を消してクラス名だけにします
    path('event_info/', EventCalendarView.as_view(), name='event_info'),
    path('event_detail/<str:event_type>/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]