from django.urls import path

from .views import *

urlpatterns = [
    path('top/', TopView.as_view(), name='topview'),
]
