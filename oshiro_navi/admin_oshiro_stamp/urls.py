from django.urls import path
from . import views
app_name = 'admin_oshiro_stamp'
urlpatterns = [
    path('oshiro_stamp_list/',views.OshiroStampListView.as_view(), name='oshiro_stamp_list'),
    path('oshiro_stamp_update/success/',views.OshiroStampUpdateSuccessView.as_view(),name='oshiro_stamp_update_success'),
    path('oshiro_stamp_update/<int:stamp_id>/',views.OshiroStampUpdateView.as_view(), name='oshiro_stamp_update'),
]