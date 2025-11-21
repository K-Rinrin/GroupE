from django.urls import path

from .views import *

urlpatterns = [
    path('top/', OperatorTopView.as_view(), name='topview'),
]
