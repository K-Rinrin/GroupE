from django.urls import path

from .views import *

app_name = 'event_info_management'

urlpatterns = [
    path('admin/list/', AdminEventInfoListView.as_view(), name='admin_event_info_list'),
    path('admin/register/',AdminEventInfoRegisterView.as_view(), name='admin_event_info_register'),
    path('admin/register_success/',AdminEventInfoRegisterSuccessView.as_view(), name='admin_event_info_register_success'),
    path('admin/update/',AdminEventInfoUpdateView.as_view(), name='admin_event_info_update'),
    path('admin/update_success/',AdminEventInfoUpdateSuccessView.as_view(), name='admin_event_info_update_success'),
    path('admin/delete/',AdminEventInfoDeleteView.as_view(), name='admin_event_info_delete'),
    path('admin/delete_check/',AdminEventInfoDeleteCheckView.as_view(), name='admin_event_info_delete_check'),
    path('admin/delete_success/',AdminEventInfoDeleteSuccessView.as_view(), name='admin_event_info_delete_success'),

    path('operator/list/', OperatorEventInfoListView.as_view(), name='operator_event_info_list'),
    path('operator/register/',OperatorEventInfoRegisterView.as_view(), name='operator_event_info_register'),
    path('operator/register_success/',OperatorEventInfoRegisterSuccessView.as_view(), name='operator_event_info_register_success'),
    path('operator/update/<int:pk>/',OperatorEventInfoUpdateView.as_view(), name='operator_event_info_update'),
    path('operator/update_success/',OperatorEventInfoUpdateSuccessView.as_view(), name='operator_event_info_update_success'),
    path('operator/delete/<int:pk>/',OperatorEventInfoDeleteView.as_view(), name='operator_event_info_delete'),
    path('operator/delete_check/',OperatorEventInfoDeleteCheckView.as_view(), name='operator_event_info_delete_check'),
    path('operator/delete_success/',OperatorEventInfoDeleteSuccessView.as_view(), name='operator_event_info_delete_success'),
]
