from django.urls import path

from .views import *

app_name = "operator_accounts"

urlpatterns = [
    path('',OperatorLoginView.as_view(), name='operator_login'),
    path('logout/',OperatorLogoutView.as_view(), name='operator_logout'),
    path('top/', OperatorTopView.as_view(), name='top'),
    path('top/list/', AdminAccountListView.as_view(), name='account_list'),
    path('top/list/create/',AdminAccountCreateView.as_view(), name='account_create'),
    path('top/list/create/success/',AdminAccountCreateSuccessView.as_view(), name='account_create_success'),
    path('top/list/delete/<int:pk>/', AdminAccountDeleteView.as_view(), name='account_delete'),
    path('top/list/delete/success/', AdminAccountDeleteSuccessView.as_view(), name='account_delete_success'),

]
