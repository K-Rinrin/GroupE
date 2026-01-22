from django.urls import path
from . import views

app_name = "admin_area_map"

urlpatterns = [
    # ★引数なし：周辺MAPトップ（城を選択）
    path("area_map/", views.AreaMapTopView.as_view(), name="area_map"),

    # ★城別：周辺MAP一覧
    path("area_map/<int:basic_info_id>/", views.AreaMapInfoListView.as_view(), name="area_map_detail"),

    # 登録（城別）
    path("area_map/<int:basic_info_id>/registar/", views.AreaMapInfoRegistarView.as_view(), name="area_map_info_registar"),
    path("area_map/<int:basic_info_id>/registar/success/", views.AreaMapInfoRegistarSuccessView.as_view(), name="area_map_info_registar_success"),

    # 更新
    path("area_map/update/<int:pk>/", views.AreaMapInfoUpdateView.as_view(), name="area_map_info_update"),
    path("area_map/update/<int:pk>/success/", views.AreaMapInfoUpdateSuccessView.as_view(), name="area_map_info_update_success"),

    # 削除
    path("area_map/delete/<int:pk>/", views.AreaMapInfoDeleteView.as_view(), name="area_map_info_delete"),
    path("area_map/<int:basic_info_id>/delete/success/",views.AreaMapInfoDeleteSuccessView.as_view(),name="area_map_info_delete_success"),
]
