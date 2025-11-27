from django.urls import path

from .views import *

app_name = "admin_accounts"

urlpatterns = [
    path('top/', AdminTopView.as_view(), name='top'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/confirm/', ContactConfirmView.as_view(), name='contact_confirm')

]
