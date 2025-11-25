from django.urls import path
from .views import *

app_name = 'admin_audio_guide'

urlpatterns = [

    # 音声ガイド一覧ページ
    path('audio_guide/', AudioGuideListtView.as_view(), name='udio_guide'),


    # 音声ガイドP登録ページ
    path('audio_guide_registar/', 
         AudioGuideRegistarView.as_view(), name='audio_guide_registar'),

    # 周辺MAP登録完了ページ
    path('audio_guide_registar_success/', 
         AudioGuideRegistarSuccessView.as_view(), name='audio_guide_registar_success'),


    # 周辺MAP更新ページ
    path('audio_guide_update/', 
         AudioGuideUpdateView.as_view(), name='audio_guide_update'),

    # 周辺MAP更新完了ページ
    path('audio_guide_update_success/', 
         AudioGuideUpdateSuccessView.as_view(), name='audio_guide_update_success'),


    # 周辺MAP削除ページ
    path('audio_guide_delete/', 
         AudioGuideDeleteView.as_view(), name='audio_guide_delete'),

    # 周辺MAP削除完了ページ
    path('audio_guide_delete_success/', 
         AudioGuideUpdateSuccessView.as_view(), name='audio_guide_delete_success'),
    
]
