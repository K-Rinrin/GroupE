from django.urls import path

from .views import *

app_name = "admin_accounts"

urlpatterns = [
    path('top/', AdminTopView.as_view(), name='top'),
    

]
