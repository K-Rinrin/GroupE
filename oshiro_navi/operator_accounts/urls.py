from django.urls import path

from .views import *

urlpatterns = [
    path('operatortop/', OperatorTopView.as_view(), name='operatortop'),
    path('operatortop/account_list', AdminAccountListView.as_view(), name='account_list'),

]
