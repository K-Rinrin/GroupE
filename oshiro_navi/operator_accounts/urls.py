from django.urls import path

from .views import *

urlpatterns = [
    path('top/', OperatorTopView.as_view(), name='top'),
    path('top/list', AdminAccountListView.as_view(), name='account_list'),
    path('top/list/delete', AdminAccountDeleteView.as_view(), name='account_delete'),


]
