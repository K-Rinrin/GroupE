from django.urls import path
from . import views  # viewsをモジュールとしてインポートする方法に統一するのが安全です

app_name = "usermy_page"

urlpatterns = [
    path('mypage/', views.MyPageTopView.as_view(), name='mypage'),
    path('mylistregistar/', views.MyListRegistarView.as_view(), name='mylistregistar'), 
    path('mylistdeletecheck/<int:pk>/', views.MyListDeleteCheckView.as_view(), name='mylistdeletecheck'),
    path('oshirostampregistar/', views.UserOshiroStampRegistar.as_view(), name='oshirostampregistar'),
    path('profileupdate/', views.ProfileCompleteView.as_view(), name='profileupdate'),
    path('profile/', views.ProfileEditView.as_view(), name='profile'),
    path('mylistdelete/', views.MyListDeleteView.as_view(), name='mylistdelete'),
    
]