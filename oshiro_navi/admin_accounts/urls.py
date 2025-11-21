from django.urls import path

from .views import *

urlpatterns = [
    path('top/', AdminTopView.as_view(), name='admintop'),

]
