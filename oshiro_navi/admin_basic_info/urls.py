from django.urls import path
from . import views

app_name = "admin_basic_info"

urlpatterns = [
    path("basic_info_list/", views.BasicInfoListView.as_view(), name="basic_info_list"),
    path("basic_info_update/", views.BasicInfoUpdateView.as_view(), name="basic_info_update"),
    path("basic_info_update/success/", views.BasicInfoUpdateSuccessView.as_view(), name="basic_info_update_success"),
]
