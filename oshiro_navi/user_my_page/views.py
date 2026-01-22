from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from admin_oshiro_stamp.models import OshiroStamp
from user_accounts.models import User
from user_accounts.models import User as UserProfile
from operator_oshiro_info.models import OshiroInfo
from user_my_list.models import OshiroMyList 
from django.http import JsonResponse
from django.utils import timezone
from admin_oshiro_stamp.models import OshiroStampInfo
from operator_oshiro_info.models import OshiroInfo
from django.views.generic import ListView

import math


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
        
        current_mylist = OshiroMyList.objects.filter(user=user_profile).select_related('oshiro_info')
        registered_ids = current_mylist.values_list('oshiro_info_id', flat=True)

        keyword = request.GET.get('keyword', '').strip()

        available_castles = OshiroInfo.objects.exclude(id__in=registered_ids)

        if keyword:
            available_castles = available_castles.filter(
                Q(oshiro_name__icontains=keyword) | Q(address__icontains=keyword)
            )

        return render(request, 'my_list_registar.html', {
            'current_mylist': current_mylist,
            'available_castles': available_castles,
            'keyword': keyword,
            'profile': user_profile
        })

    def post(self, request):
        # (POST部分は変更なしで大丈夫です)
        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        castle_ids = request.POST.getlist('castle_ids')

        if not castle_ids:
            messages.error(request, "お城を選択して下さい")
            return self.get(request)

        for castle_id in castle_ids:
            oshiro = get_object_or_404(OshiroInfo, id=castle_id)
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
    
# --- 5. 他ユーザープロフィール表示 ---
class UserProfileView(View):
    def get(self, request, user_id):
    
        target_user = get_object_or_404(User, id=user_id)
        
        my_list = OshiroMyList.objects.filter(user=target_user).select_related('oshiro_info')
        
        stamps = OshiroStamp.objects.filter(user=target_user).select_related('oshiro_stamp_info')

        return render(request, 'other_user_profile.html', {
            'target_user': target_user,
            'my_list': my_list,
            'stamps': stamps,
        })



# --- 6. スタンプ取得処理 ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球の半径（メートル）
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class GetStampView(LoginRequiredMixin, View):
    def post(self, request):  # 引数から oshiro_id を削除
        try:
            user_lat = float(request.POST.get('latitude'))
            user_lng = float(request.POST.get('longitude'))
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': '位置情報が取得できませんでした。'})

        # 登録されている全てのお城を取得
        all_castles = OshiroInfo.objects.all()
        target_oshiro = None

        # ループして1km以内のお城を探す
        for oshiro in all_castles:
            if oshiro.latitude and oshiro.longitude:
                dist = calculate_distance(user_lat, user_lng, oshiro.latitude, oshiro.longitude)
                if dist <= 1000:  # 1000m以内ならヒット
                    target_oshiro = oshiro
                    break  # 最初に見つかったお城で終了

        # 近くにお城がなかった場合
        if not target_oshiro:
            return JsonResponse({'status': 'error', 'message': '近くにスタンプが押せるお城がありません（半径1km以内）。'})

        # --- 以下、スタンプ付与処理 ---
        stamp_info = OshiroStampInfo.objects.filter(oshiro_info=target_oshiro).first()
        if not stamp_info:
            return JsonResponse({'status': 'error', 'message': f'「{target_oshiro.oshiro_name}」はスタンプの準備ができていません。'})

        user_profile, _ = UserProfile.objects.get_or_create(account=request.user)
        
        # すでに持っているかチェック
        if OshiroStamp.objects.filter(oshiro_stamp_info=stamp_info, user=user_profile).exists():
            return JsonResponse({'status': 'info', 'message': f'「{target_oshiro.oshiro_name}」のスタンプは既に獲得済みです！'})

        # スタンプ作成
        OshiroStamp.objects.create(
            oshiro_stamp_info=stamp_info,
            user=user_profile,
            oshiro_stamp=1,
            date=timezone.now().date()
        )

        return JsonResponse({'status': 'success', 'message': f'やった！「{target_oshiro.oshiro_name}」のスタンプをゲットしました！'})
    
class OshiroStampBookView(LoginRequiredMixin, ListView):
    model = OshiroStamp
    template_name = "user_oshiro_stamp_registar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 全スタンプ取得
        all_stamps = OshiroStamp.objects.filter(user__account=self.request.user).order_by('date')
        
        # URLの ?page= の数字を取得。なければ1ページ目。
        try:
            page = int(self.request.GET.get('page', 1))
        except:
            page = 1
            
        # 1ページ6個ずつ表示するための切り出し
        start = (page - 1) * 6
        end = start + 6
        context['stamps_on_page'] = all_stamps[start:end]
        
        # そのページの空き枠数
        context['range_remaining'] = range(6 - context['stamps_on_page'].count())
        
        # ページ移動用のデータ
        context['current_page'] = page
        context['prev_page'] = page - 1
        context['next_page'] = page + 1
        context['total_count'] = all_stamps.count()
        
        return context

# --- 5. 完了画面・その他 ---
class ProfileCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile_update.html'

class MyListDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "my_list_delete.html"
