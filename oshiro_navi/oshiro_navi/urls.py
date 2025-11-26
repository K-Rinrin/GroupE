"""oshiro_navi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_site/', admin.site.urls),

    # --- 運営アカウント機能 ---
    path('operator/', include('operator_accounts.urls')),

    # # --- お城情報管理 ---
    path('operator/oshiro/', include('operator_oshiro_info.urls')),

    # --- 管理者アカウント機能 ---
    path('admin/', include('admin_accounts.urls')),

    # --- 管理者周辺MAP機能 ---
    path('admin/area_map/', include('admin_area_map.urls')),

    # # --- 管理者音声ガイド機能 ---
    path('admin/audio_guide/', include('admin_audio_guide.urls')),

    # --- 管理者お城スタンプ機能 ---
    path("admin_oshiro_stamp/", include("admin_oshiro_stamp.urls")),

    # # --- 管理者モデルコース機能 ---
    path('admin/model_course/', include('admin_model_course.urls')),

    # # --- 管理者基本情報機能 ---
    path('admin/basic_info/', include('admin_basic_info.urls')),

    # # --- 利用者アカウント機能 ---
    path('user/', include('user_accounts.urls')),

    # # --- 利用者音声ガイド機能 ---
    # path('user/audio_guide/', include('user_audio_guide.urls')),

    # # --- 利用者モデルコース機能 ---
    # path('user/model_course/', include('user_model_course.urls')),
    
    # # --- 利用者お城リスト機能 ---
    path('usermy_list/', include('user_my_list.urls')),
    
    # # --- 利用者マイページ機能 ---
    path('usermy_page/', include('user_my_page.urls')),

    # # --- イベント情報機能 ---
    path('event_management/', include('event_info_management.urls')),

]
