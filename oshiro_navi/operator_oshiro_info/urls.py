from django.urls import path

from .views import *

app_name = "operator_oshiro_info"

urlpatterns = [
    path('list/',OshiroInfoListView.as_view(), name='list'),
    path('register/',OshiroInfoRegisterView.as_view(), name='register'),
    path('register_success/',OshiroInfoRegisterSuccessView.as_view(), name='register_success'),
    path('更新/',OshiroInfoUpdateView.as_view(), name='update'),
    path('更新完了/',OshiroInfoUpdateSuccessView.as_view(), name='update_success'),





]
