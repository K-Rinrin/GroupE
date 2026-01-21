from django.urls import path
from .views import *

app_name = "usermy_list"

urlpatterns = [ 
    path('oshirolist/', OshirolistView.as_view(), name='oshirolist'),
    path('oshiro_info/<int:pk>/', OshiroInfoView.as_view(), name='oshiroinfo'),
    path('oshiro_basic_info/<int:pk>/', OshiroBasicInfoView.as_view(), name='oshirobasicinfo'),
    path('review/<int:pk>/', OshiroReviewView.as_view(), name='oshiroreview'),
    path('oshiroaftersearch/', OshiroAfterSearchView.as_view(), name='aftersearch'),
    path('oshiromap/<int:pk>/', OshiroMapView.as_view(), name='oshiromap'),
    path('review/delete/<int:pk>/', delete_review, name='delete_review'),
]