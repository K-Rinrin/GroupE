from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404
from admin_accounts.models import Admin
from .models import OshiroStampInfo
from operator_oshiro_info.models import OshiroInfo  # お城情報の参照用
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied





def _get_or_404(model_cls, **kwargs):
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")

# --- Viewクラス ---

class OshiroStampListView(LoginRequiredMixin, View):
    def get(self, request):
        if not hasattr(request.user, 'admin_profile'):
            return render(request, "oshiro_stamp_list.html", {"stamps": []})
        
        admin_profile = request.user.admin_profile

        # 担当しているお城（1〜5）をリスト化（Noneを除外）
        managed_castle_ids = [
            admin_profile.oshiro_management1_id,
            admin_profile.oshiro_management2_id,
            admin_profile.oshiro_management3_id,
            admin_profile.oshiro_management4_id,
            admin_profile.oshiro_management5_id,
        ]
        managed_castle_ids = [cid for cid in managed_castle_ids if cid is not None]

        # 担当お城のIDリストに含まれるOshiroInfoのみ取得
        oshiros = OshiroInfo.objects.filter(id__in=managed_castle_ids).order_by("id")

        stamps = []
        for oshiro in oshiros:
            stamp = OshiroStampInfo.objects.filter(oshiro_info=oshiro).first()
            stamps.append({"oshiro": oshiro, "stamp": stamp})

        return render(request, "oshiro_stamp_list.html", {"stamps": stamps})




class OshiroStampUpdateSuccessView(LoginRequiredMixin,TemplateView):
    template_name = "oshiro_stamp_update_success.html"


class OshiroStampUpdateView(LoginRequiredMixin, View):
    def get(self, request, oshiro_id):
        # お城情報を取得
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        # そのお城に紐づくスタンプがあるか確認（なければNone）
        stamp = OshiroStampInfo.objects.filter(oshiro_info=oshiro).first()
        
        return render(request, "oshiro_stamp_update.html", {
            "stamp": stamp,
            "oshiro": oshiro,  # スタンプがない場合でも、どのお城用か表示するために渡す
        })

    def post(self, request, oshiro_id):
        if request.POST.get("cancel"):
            return redirect("admin_oshiro_stamp:oshiro_stamp_list")

        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        
        # get_or_createではなく、まず存在確認だけ行う
        stamp = OshiroStampInfo.objects.filter(oshiro_info=oshiro).first()

        stamp_name = request.POST.get("stamp_name")
        stamp_image = request.FILES.get("stamp_image")

        # --- バリデーション ---
        errors = []
        if not stamp_name:
            errors.append("スタンプ名は必須項目です")

        # 画像のチェック：
        # 「既存の画像がない(stampが未作成、またはimageが空)」かつ「新しい画像も送られていない」場合
        has_existing_image = stamp and stamp.oshiro_stamp_image
        if not has_existing_image and not stamp_image:
            errors.append("スタンプ画像を選択してください")

        if errors:
            return render(request, "oshiro_stamp_update.html", {
                "stamp": stamp,
                "oshiro": oshiro,
                "errors": errors, # リストで渡すと複数のエラーを表示できて便利です
            })

        # --- データの更新・保存 ---
        if not stamp:
            # 新規作成
            stamp = OshiroStampInfo(oshiro_info=oshiro, admin=request.user.admin_profile)
        
        stamp.stamp_name = stamp_name
        stamp.admin = request.user.admin_profile 
        
        if stamp_image:
            stamp.oshiro_stamp_image = stamp_image
            
        stamp.save()

        return redirect("admin_oshiro_stamp:oshiro_stamp_update_success")
