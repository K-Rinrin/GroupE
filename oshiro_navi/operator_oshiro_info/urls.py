from django.urls import path

from .views import *

app_name = "operator_oshiro_info"

urlpatterns = [
    path('list/',OshiroInfoListView.as_view(), name='list'),
    path('register/',OshiroInfoRegisterView.as_view(), name='register'),
    path('register_success/',OshiroInfoRegisterSuccessView.as_view(), name='register_success'),
    path('update/',OshiroInfoUpdateView.as_view(), name='update'),
    path('update_success/',OshiroInfoUpdateSuccessView.as_view(), name='update_success'),





]
