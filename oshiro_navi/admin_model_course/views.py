from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# モデルのインポート
from .models import ModelCourse
from operator_oshiro_info.models import OshiroInfo # お城情報のモデル


try:
    # 管理者モデル
    from admin_accounts.models import Admin
except ImportError:
    pass

try:
    # モデルコースモデル 
    from .models import ModelCourse
except ImportError:
    pass



# お城選択（担当するお城のみ表示）
class ModelCouseSearchView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ログイン中のユーザー情報を取得
        user = self.request.user
        
        try:
            # 1. ログインユーザーに紐づく管理者(Admin)レコードを取得
            # テーブル定義書より: accountカラム(OneToOne)で特定
            admin_record = Admin.objects.get(account=user)
            
            # 2. 横持ちのカラム (oshiro_manegement1 ~ 5) をリスト化
            potential_castles = [
                admin_record.oshiro_management1,
                admin_record.oshiro_management2,
                admin_record.oshiro_management3,
                admin_record.oshiro_management4,
                admin_record.oshiro_management5
            ]

            # 3. None（未設定の枠）を除外し、有効なOshiroInfoオブジェクトのみ抽出
            my_castles = [castle for castle in potential_castles if castle is not None]
            
            
            context['rows'] = my_castles

        except Admin.DoesNotExist:
            # 管理者データが存在しない場合
            context['rows'] = []
            context['error_message'] = "管理者情報が見つかりませんでした。"
        
        except Exception as e:
            context['rows'] = []
            context['error_message'] = f"予期せぬエラーが発生しました: {e}"

        return context


# 一覧
class ModelCouseListView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # URLから渡された oshiro_id を取得
        oshiro_id = self.kwargs.get('oshiro_id')
        
        # お城情報を取得（画面にお城の名前を出すためなど）
        oshiro = get_object_or_404(OshiroInfo, pk=oshiro_id)
        
        # そのお城に紐づくモデルコースを取得してセット
        model_courses = ModelCourse.objects.filter(oshiro_info=oshiro)
        
        context['oshiro'] = oshiro
        context['rows'] = model_courses
        
        return context


# 新規登録
class ModelCouseRegistarView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar.html"


# 新規登録完了
class ModelCouseRegistarSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar_success.html"


# 編集（更新）
class ModelCouseUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update.html"


# 編集完了
class ModelCouseUpdateSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update_success.html"