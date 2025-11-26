from django.urls import path

from .views import *

app_name = "user_audio_guide"

urlpatterns = [
    path('guide_list/',AudioGUideListView.as_view(), name='guide_list'),
    path('qr_scan/',QrScanView.as_view(), name='qr_scan'),

]
