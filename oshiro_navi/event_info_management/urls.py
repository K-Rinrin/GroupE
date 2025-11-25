from django.urls import path

from .views import *

app_name = 'event_info_management'

urlpatterns = [
    path('list/', EventInfoListView.as_view(), name='event_info_list'),
    path('register/',EventInfoRegisterView.as_view(), name='event_info_register'),
    path('register_success/',EventInfoRegisterSuccessView.as_view(), name='event_info_register_success'),
    path('update/',EventInfoUpdateView.as_view(), name='event_info_update'),
    path('update_success/',EventInfoUpdateSuccessView.as_view(), name='event_info_update_success'),
    path('delete/',EventInfoDeleteView.as_view(), name='event_info_delete'),
    path('delete_check/',EventInfoDeleteCheckView.as_view(), name='event_info_delete_check'),
    path('delete_success/',EventInfoDeleteSuccessView.as_view(), name='event_info_delete_success'),
]
