from django.urls import path

from .views import *

app_name = "operator_accounts"

urlpatterns = [
    path('',OperatorLoginView.as_view(), name='operator_login'),
    path('logout/',OperatorLogoutView.as_view(), name='operator_logout'),
    path('top/', OperatorTopView.as_view(), name='top'),
    path('top/contact/list/', OperatorContactList.as_view(), name='contact_list'),
    path('top/contact/form/', OperatorContactForm.as_view(), name='contact_form'),
    path('top/contact/confirm/', OperatorContactConfirm.as_view(), name='contact_confirm'),
    path('top/list/', AdminAccountListView.as_view(), name='account_list'),
    path('top/list/create/',AdminAccountCreateView.as_view(), name='account_create'),
    path('top/list/create/success/',AdminAccountCreateSuccessView.as_view(), name='account_create_success'),
    path('top/list/delete/', AdminAccountDeleteView.as_view(), name='account_delete'),
    path('top/list/delete/success/', AdminAccountDeleteSuccessView.as_view(), name='account_delete_success'),

]
