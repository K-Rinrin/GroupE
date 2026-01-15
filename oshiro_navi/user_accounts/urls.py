from django.urls import path

from .views import *

app_name = "user_accounts"

urlpatterns = [

    # ユーザーTop画面
    path('top/', UserTopView.as_view(), name='top'),

    # ログアウト画面
    path('logout/', UserlogoutView.as_view(), name='logout'),
    path('logout_check/', UserlogoutCheckView.as_view(), name='logout_check'),

    # サインアップ・ログイン画面
    path('account/', UserAccountView.as_view(), name='account'),
    
]
