from django.urls import path
from . import views

app_name = "admin_model_course"

urlpatterns = [
    
    path("list/", views.ModelCouseListView.as_view(), name="model_couse_list"),

    # 新規登録
    path("registar/", views.ModelCouseRegistarView.as_view(), name="model_couse_registar"),

    # 新規登録完了
    path("registar/success/", views.ModelCouseRegistarSuccessView.as_view(),
         name="model_couse_registar_success"),

    # 編集（更新）
    path("update/", views.ModelCouseUpdateView.as_view(), name="model_couse_update"),

    # 編集完了
    path("update/success/", views.ModelCouseUpdateSuccessView.as_view(),
         name="model_couse_update_success"),
]
