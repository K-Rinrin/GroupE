from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

# モデルのインポート
from operator_oshiro_info.models import OshiroInfo
from admin_basic_info.models import BasicInfo
from admin_area_map.models import AreaMapInfo 
from user_accounts.models import UserReview, User
from .forms import UserReviewForm 

# 1. お城検索画面
class OshirolistView(LoginRequiredMixin, TemplateView):
    template_name = "oshiro_list.html"

# 2. お城検索結果画面
class OshiroAfterSearchView(LoginRequiredMixin, ListView):
    model = OshiroInfo
    template_name = "oshiro_after_search.html"
    context_object_name = "oshiro_list"  

    def get_queryset(self):
        # 検索ボタンから送られてきたキーワードを取得
        keyword = self.request.GET.get('keyword', '')
        
        if keyword:
            # キーワードがある場合は、名前か住所に含まれるものを絞り込む
            return OshiroInfo.objects.filter(
                Q(oshiro_name__icontains=keyword) | Q(address__icontains=keyword)
            )
        
    
        return OshiroInfo.objects.all()
# 3. お城詳細情報画面
class OshiroInfoView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_info.html"
    context_object_name = "oshiro"

# 4. 基本情報画面
class OshiroBasicInfoView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_basic_info.html"
    context_object_name = "oshiro"

# 5. 口コミ画面（表示・投稿制限・削除対応）
class OshiroReviewView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "user_review.html"
    context_object_name = "oshiro"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = UserReview.objects.filter(oshiro_info=self.object).order_by('-post_date_time')
        context['reviews'] = reviews
        
        avg_score = reviews.aggregate(Avg('five_star_review'))['five_star_review__avg']
        context['avg_score'] = round(avg_score, 1) if avg_score else 0.0

        # --- 更新モードの判定 ---
        # URLのパラメータに ?edit_id=◯◯ がついているかチェック
        edit_id = self.request.GET.get('edit_id')
        user_profile = User.objects.filter(account=self.request.user).first()
        
        if edit_id:
            # 更新用：そのIDの口コミを探してフォームに入れる
            edit_review = get_object_or_404(UserReview, id=edit_id, user=user_profile)
            context['form'] = UserReviewForm(instance=edit_review)
            context['edit_mode'] = True # 今は更新中だよ！という目印
            context['edit_id'] = edit_id
        else:
            # 新規用
            context['form'] = UserReviewForm()
            context['edit_mode'] = False

        # 現在このお城に口コミがあるか（更新モードの時は「投稿済み」メッセージを出さないようにする）
        has_posted = UserReview.objects.filter(oshiro_info=self.object, user=user_profile).exists()
        context['has_posted'] = has_posted
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_profile, _ = User.objects.get_or_create(account=request.user)
        
        # --- 更新か新規かの判定 ---
        edit_id = request.GET.get('edit_id')
        if edit_id:
            # 更新処理
            instance = get_object_or_404(UserReview, id=edit_id, user=user_profile)
            form = UserReviewForm(request.POST, request.FILES, instance=instance)
        else:
            # 新規投稿処理（二重投稿チェック付き）
            if UserReview.objects.filter(oshiro_info=self.object, user=user_profile).exists():
                messages.error(request, "口コミの投稿は一人一回までです。")
                return redirect('usermy_list:oshiroreview', pk=self.object.pk)
            form = UserReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.oshiro_info = self.object
            review.user = user_profile
            review.save()
            return redirect('usermy_list:oshiroreview', pk=self.object.pk)
        
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

# ★ 口コミ削除用の関数
def delete_review(request, pk):
    review = get_object_or_404(UserReview, id=pk)
    # 本人（Account）だけが削除可能
    if review.user.account == request.user:
        review.delete()
        messages.success(request, "口コミを削除しました。")
    return redirect('usermy_list:oshiroreview', pk=review.oshiro_info.pk)

# 6. お城周辺MAP画面
class OshiroMapView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_map.html"
    context_object_name = "oshiro"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basic_info = getattr(self.object, 'basicinfo', None)
        pins_data = []
        if basic_info:
            map_items = AreaMapInfo.objects.filter(basic_info=basic_info)
            for item in map_items:
                pins_data.append({
                    'name': item.icon_name,
                    'category': item.icon_name,
                    'lat': item.latitude,
                    'lng': item.longitude,
                    'image': item.icon_image.url if item.icon_image else None,
                })
        
        context['pins_json'] = json.dumps(pins_data, cls=DjangoJSONEncoder)
        context['center'] = pins_data[0] if pins_data else {"lat": 37.4879, "lng": 139.9290}
        return context