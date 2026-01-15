from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# 以前のコードに基づき、UserProfileモデルを使用
from user_accounts.models import User as UserProfile

class MyPageTopView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        return render(request, 'mypage.html', {'user': profile})

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        # 変数名を 'user' から 'profile' に変更
        return render(request, 'user_profile.html', {
            'profile': profile 
        })

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        
        bio_data = request.POST.get('bio', '')
        icon_data = request.FILES.get('icon')

        # 自己紹介未入力チェック
        if not bio_data or bio_data.strip() == "":
            messages.error(request, "自己紹介を入力してください")
            profile.user_about = ""  # 画面上の表示を空にする
            return render(request, 'user_profile.html', {
            'profile': profile
        })

        # DB更新
        profile.user_about = bio_data
        
        # 新しい画像が選択された場合のみ更新
        if icon_data:
            profile.profile_image = icon_data
        
        profile.save()
        return redirect('usermy_page:profileupdate') # 完了画面への名前を確認

class ProfileCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile_update.html'
    """
    更新完了画面
    """
    template_name = 'user_profile_update.html'

class ProfileCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile_update.html'
    
class MypageView(TemplateView):
    template_name = "mypage.html"

class MyListRegistarView(TemplateView):
    template_name = "my_list_registar.html"

class MyListDeleteCheckView(TemplateView):
    template_name = "my_list_delete_check.html"

class UserOshiroStampRegistar(TemplateView):
    template_name = "user_oshiro_stamp_registar.html"

class MyListDeleteView(TemplateView):
    template_name = "my_list_delete.html"