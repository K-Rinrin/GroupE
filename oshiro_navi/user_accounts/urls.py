from django.urls import path

from .views import *

urlpatterns = [
    path('top/', UserTopView.as_view(), name='top'),
]
