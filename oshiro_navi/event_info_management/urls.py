from django.urls import path

from .views import *

urlpatterns = [
    path('event_info_management/', EventInfoManagementView.as_view(), name='event_info_management'),
]
