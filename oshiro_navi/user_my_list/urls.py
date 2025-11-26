from django.urls import path

from .views import *

app_name = "usermy_list"

urlpatterns = [ 
    path('oshirolist/', OshirolistView.as_view(), name='oshirolist'),
    path('oshiroinfo/', OshiroInfoView.as_view(), name='oshiroinfo'),
    path('aftersearch/', OshiroAfterSearchView.as_view(), name='oshiroaftersearch'),
    path('oshirobasicinfo/', OshiroBasicInfoView.as_view(), name='oshirobasicinfo'),
    path('review/', OshiroReviewView.as_view(), name='oshiroreview'),

]
