from django.urls import path

from .views import *

app_name = "user_audio_guide"

urlpatterns = [
    path('oshiro_list/', UserAudioGuideOshiroListView.as_view(), name='oshiro_list'),
    path('guide_list/<int:oshiro_id>/',UserAudioGuideListView.as_view(), name='guide_list'),
    path('qr_scan/',QrScanView.as_view(), name='qr_scan'),

]
