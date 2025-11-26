from django.urls import path

from .views import *

app_name = "user_accounts"

urlpatterns = [
    path('top/', UserTopView.as_view(), name='top'),
    path('logout/', UserlogoutView.as_view(), name='logout'),
    path('account/', UserAccountView.as_view(), name='account'),
    
]
