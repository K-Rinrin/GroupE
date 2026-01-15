from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

# モデルのインポート
from user_accounts.models import User as UserProfile
from operator_oshiro_info.models import OshiroInfo
from user_my_list.models import OshiroMyList 

# --- 1. マイページトップ ---
class MyPageTopView(LoginRequiredMixin, View):
    def get(self, request):
        # request.user(Account) から UserProfile を取得
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        return render(request, 'mypage.html', {'profile': profile})

# --- 2. プロフィール編集 ---
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        return render(request, 'user_profile.html', {'profile': profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(account=request.user)
        bio_data = request.POST.get('bio', '')
        icon_data = request.FILES.get('icon')

        if not bio_data or bio_data.strip() == "":
            messages.error(request, "自己紹介を入力してください")
            profile.user_about = "" 
            return render(request, 'user_profile.html', {'profile': profile})

        profile.user_about = bio_data
        if icon_data:
            profile.profile_image = icon_data
        profile.save()
        return redirect('usermy_page:profileupdate')

# --- 3. お城マイリスト：検索・登録画面 ---
class MyListRegistarView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        
        # 1. 現在のマイリスト（下のリスト）は常に表示
        current_mylist = OshiroMyList.objects.filter(user=user_profile).select_related('oshiro_info')
        registered_ids = current_mylist.values_list('oshiro_info_id', flat=True)

        # 2. 検索キーワードを取得
        keyword = request.GET.get('keyword', '').strip()

        # 3. キーワードがある時だけ検索し、ない時は空リストにする
        if keyword:
            available_castles = OshiroInfo.objects.exclude(id__in=registered_ids).filter(
                Q(oshiro_name__icontains=keyword) | Q(address__icontains=keyword)
            )
        else:
            # キーワードがない時は空のクエリセットを返す
            available_castles = OshiroInfo.objects.none()

        return render(request, 'my_list_registar.html', {
            'current_mylist': current_mylist,
            'available_castles': available_castles,
            'keyword': keyword,
            'profile': user_profile
        })

    def post(self, request):
        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        castle_ids = request.POST.getlist('castle_ids')

        if not castle_ids:
            messages.error(request, "お城を選択して下さい")
            return self.get(request)

        for castle_id in castle_ids:
            oshiro = get_object_or_404(OshiroInfo, id=castle_id)
            # 重複登録を防ぎつつ保存
            OshiroMyList.objects.get_or_create(
                user=user_profile,
                oshiro_info=oshiro
            )
        
        return redirect('usermy_page:mylistregistar')

    

# --- 4. お城マイリスト：削除確認・実行 ---
class MyListDeleteCheckView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        # user=user_profile で対象を特定
        item = get_object_or_404(OshiroMyList, pk=pk, user=user_profile)
        return render(request, 'my_list_delete_check.html', {
            'item': item,
            'profile': user_profile
        })

    def post(self, request, pk):
        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        item = get_object_or_404(OshiroMyList, pk=pk, user=user_profile)
        item.delete()
        return redirect('usermy_page:mylistdelete')

# --- 5. 完了画面・その他 ---
class ProfileCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile_update.html'

class MyListDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "my_list_delete.html"

class UserOshiroStampRegistar(LoginRequiredMixin, TemplateView):
    template_name = "user_oshiro_stamp_registar.html"