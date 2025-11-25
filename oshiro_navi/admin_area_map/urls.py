from django.urls import path
from .views import *

app_name = 'admin_area_map'

urlpatterns = [

    # 周辺MAP一覧ページ
    path('area_map/', AreaMapInfoListView.as_view(), name='area_map'),


    # 周辺MAP登録ページ
    path('area_map_info_registar/', 
         AreaMapInfoRegistarView.as_view(), name='area_map_info_registar'),

    # 周辺MAP登録完了ページ
    path('area_map_info_registar_success/', 
         AreaMapInfoRegistarSuccessView.as_view(), name='area_map_info_registar_success'),


    # 周辺MAP更新ページ
    path('area_map_info_update/', 
         AreaMapInfoUpdateView.as_view(), name='area_map_info_update'),

    # 周辺MAP更新完了ページ
    path('area_map_info_update_success/', 
         AreaMapInfoUpdateSuccessView.as_view(), name='area_map_info_update_success'),


    # 周辺MAP削除ページ
    path('area_map_info_delete/', 
         AreaMapInfoDeleteView.as_view(), name='area_map_info_delete'),

    # 周辺MAP削除完了ページ
    path('area_map_info_delete_success/', 
         AreaMapInfoDeleteSuccessView.as_view(), name='area_map_info_delete_success'),
    
]
