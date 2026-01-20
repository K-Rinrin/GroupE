from django.urls import path
from .views import *

app_name = 'admin_audio_guide'

urlpatterns = [

# ─────────────────────
# 城一覧
# ─────────────────────
path(
     'audio_guide/',
     AudioGuideOshiroListView.as_view(),
     name='audio_guide'
),

# ─────────────────────
# 城ごとの音声ガイド一覧
# ─────────────────────
path(
     'audio_guide/<int:oshiro_id>/',
     AudioGuideListView.as_view(),
     name='audio_guide_list'
),

# ─────────────────────
# 新規登録
# ─────────────────────
path(
     'audio_guide/<int:oshiro_id>/create/',
     AudioGuideRegistarView.as_view(),
     name='audio_guide_registar'
),

# 新規登録完了
path(
     'audio_guide/<int:oshiro_id>/create/success/',
     AudioGuideRegistarSuccessView.as_view(),
     name='audio_guide_registar_success'
),

# ─────────────────────
# 更新
# ─────────────────────
path(
     "audio_guide/<int:oshiro_id>/update/<int:audio_guide_id>/",
     AudioGuideUpdateView.as_view(),
     name="audio_guide_update"
),

# 更新完了
path(
     'audio_guide/<int:oshiro_id>/update/<int:audio_guide_id>/success/',
     AudioGuideUpdateSuccessView.as_view(),
     name='audio_guide_update_success'
),

# ─────────────────────
# 削除
# ─────────────────────
path(
     'audio_guide/<int:oshiro_id>/delete/<int:audio_guide_id>/',
     AudioGuideDeleteView.as_view(),
     name='audio_guide_delete'
),

# 削除完了
path(
     'audio_guide/<int:oshiro_id>/delete/<int:audio_guide_id>/success/',
     AudioGuideDeleteSuccessView.as_view(),
     name='audio_guide_delete_success'
),

# ─────────────────────
# QRコード生成
# ─────────────────────
path(
     'qr_generetor/',
     QRcodeGeneretorView.as_view(),
     name='qr_generetor'
),
]
