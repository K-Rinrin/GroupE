from django.urls import path
from . import views
app_name = 'admin_oshiro_stamp'
urlpatterns = [
    path('oshiro_stamp_registar/',views.OshiroStampRegistarView.as_view(), name='oshiro_stamp_registar'),
    path('oshiro_stamp_registar/success/',views.OshiroStampRegistarSuccessView.as_view(),name='oshiro_stamp_registar_success'),
]