from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from operator_oshiro_info.models import OshiroInfo
from admin_basic_info.models import BasicInfo
from django.shortcuts import redirect
from .forms import UserReviewForm 
from user_accounts.models import UserReview
from django.db.models import Avg
from admin_area_map.models import AreaMapInfo 


# 1. お城検索画面（検索窓だけがある画面）
class OshirolistView(LoginRequiredMixin, TemplateView):
    template_name = "oshiro_list.html"

# 2. お城検索結果画面（検索後にリストが出る画面）
class OshiroAfterSearchView(LoginRequiredMixin, ListView):
    model = OshiroInfo
    template_name = "oshiro_after_search.html"
    context_object_name = "oshiro_list"  

    def get_queryset(self):
        # 検索ボタンから送られてきたキーワードを取得
        keyword = self.request.GET.get('keyword', '')
        
        if keyword:
            # お城名、または住所にキーワードが含まれるものをフィルタリング
            return OshiroInfo.objects.filter(
                Q(oshiro_name__icontains=keyword) | Q(address__icontains=keyword)
            )
        # キーワードがない場合は空のリストを返す
        return OshiroInfo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索結果画面でも何を検索したか表示するためにキーワードを渡す
        context['keyword'] = self.request.GET.get('keyword', '')
        return context


# 3. お城詳細情報画面
class OshiroInfoView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_info.html"
    context_object_name = "oshiro"

# 4. 基本情報画面（管理者が登録した情報）
class OshiroBasicInfoView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_basic_info.html"
    context_object_name = "oshiro"


# 5. 口コミ画面（表示と投稿を同時に行う）
class OshiroReviewView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "user_review.html"
    context_object_name = "oshiro"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 投稿用フォームを渡す
        context['form'] = UserReviewForm()

        # --- モデル修正(oshiro_info追加)が終わるまでの暫定処理 ---
        # 本来は以下のように書きますが、今はエラーが出るのでコメントアウトします
        # reviews = UserReview.objects.filter(oshiro_info=self.object)
        # context['reviews'] = reviews.order_by('-post_date_time')
        # avg_score = reviews.aggregate(Avg('five_star_review'))['five_star_review__avg']
        # context['avg_score'] = round(avg_score, 1) if avg_score else 0.0

        # 一時的にエラーを回避するためのダミーデータ
        context['reviews'] = [] 
        context['avg_score'] = 0.0 # 初期値として0.0を表示させる
        # ---------------------------------------------------
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserReviewForm(request.POST, request.FILES)
        
        # 【修正】今は保存処理を動かさず、単に画面をリフレッシュ（リダイレクト）させるだけにする
        if form.is_valid():
            # review = form.save(commit=False)
            # review.oshiro_info = self.object  # ここでエラーが出るので停止
            # review.user = request.user.user_profile
            # review.save()
            return redirect('usermy_list:oshiroreview', pk=self.object.pk)
        
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    
class OshiroMapView(LoginRequiredMixin, DetailView):
    model = OshiroInfo
    template_name = "oshiro_map.html"
    context_object_name = "oshiro"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. このお城に紐づく「基本情報」を取得
        basic_info = getattr(self.object, 'basicinfo', None)
        
        if basic_info:
            # 2. その基本情報に紐づく「周辺MAP情報」をすべて取得
            context['map_items'] = AreaMapInfo.objects.filter(basic_info=basic_info).order_by('id')
        else:
            context['map_items'] = []
            
        return context