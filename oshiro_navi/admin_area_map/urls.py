from django.urls import path
from .views import *

app_name = 'admin_area_map'

urlpatterns = [
    path('area_map/', AreaMapInfoListView.as_view(), name='area_map'),
]
