from django.urls import path

from .views import *

app_name = "user_event_info"

urlpatterns = [
    path('event_info/',UserEventInfoView.as_view(), name='event_info'),

]
