from django.urls import path

from .views import *

app_name = "user_event_info"

urlpatterns = [
    path('event_info/',EventCalendarView.as_view(), name='event_info'),
    path('event_detail/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

]
