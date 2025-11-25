from django.urls import path

from .views import *

app_name = "usermy_page"

urlpatterns = [
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('mylistregistar/', MyListRegistarView.as_view(), name='mylistregistar'), 
    path('mylistdeletecheck/', MyListDeleteCheckView.as_view(), name='mylistdeletecheck'),
    path('oshirostampregistar/', UserOshiroStampRegistar.as_view(), name='oshirostampregistar'),
    path('profileupdate/', UserProfileUpdateView.as_view(), name='profileupdate'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('mylistdelete/', MyListDeleteView.as_view(), name='mylistdelete'),


]
