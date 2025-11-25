from django.urls import path

from .views import *

urlpatterns = [
    path('mypage/', MypageView.as_view(), name='mypage'),

    path('mylistregistar/', MyListRegistarView.as_view(), name='mylistregistar'),
    
    path('mylistdeletecheck/', MyListDeleteCheckView.as_view(), name='mylistdeletecheck'),

    path('oshirostampregistar/', OshiroStampRegistar.as_view(), name='oshirostampregistar'),

    path('profileupdate/', UserProfileUpdateView.as_view(), name='profileupdate'),


]
