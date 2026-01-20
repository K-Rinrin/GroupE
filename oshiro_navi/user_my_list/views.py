from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from operator_oshiro_info.models import OshiroInfo

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

# --- 以下、詳細ボタンを押した後の各画面 ---

# 詳細ハブ画面（お城情報・基本情報・口コミへのリンクがある画面）
class OshiroHubView(LoginRequiredMixin, TemplateView):
    template_name = "oshiro_hub.html"
    # ※実際には pk からお城を特定するロジックを後で追加します

# お城情報画面（運営が登録した情報）
class OshiroInfoView(LoginRequiredMixin, TemplateView):
    template_name = "oshiro_info.html"

# 基本情報画面（管理者が登録した情報）
class OshiroBasicInfoView(LoginRequiredMixin, TemplateView):
    template_name = "oshiro_basic_info.html"

# 口コミ画面（利用者が投稿した情報）
class OshiroReviewView(LoginRequiredMixin, TemplateView):
    template_name = "user_review.html"