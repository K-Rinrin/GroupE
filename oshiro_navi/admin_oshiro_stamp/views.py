from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404
from admin_accounts.models import Admin
from .models import OshiroStampInfo
from operator_oshiro_info.models import OshiroInfo  # お城情報の参照用
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class AdminOshiroRequiredMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            admin_record = Admin.objects.get(account=user)
            potential_castles = [
                admin_record.oshiro_management1,
                admin_record.oshiro_management2,
                admin_record.oshiro_management3,
                admin_record.oshiro_management4,
                admin_record.oshiro_management5
            ]
            my_castles = [c for c in potential_castles if c is not None]
            context['rows'] = my_castles
        except Admin.DoesNotExist:
            context['rows'] = []
            context['error_message'] = "管理者情報が見つかりませんでした。"
        except Exception as e:
            context['rows'] = []
            context['error_message'] = f"エラー: {e}"
        return context


def _get_or_404(model_cls, **kwargs):
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")

# --- Viewクラス ---

class OshiroStampListView(AdminOshiroRequiredMixin,LoginRequiredMixin,View):
    """お城スタンプ一覧"""
    def get(self, request):
        # OneToOneの関係にあるお城情報もまとめて取得
        stamps = OshiroStampInfo.objects.all().select_related('oshiro_info').order_by("id")
        return render(request, "oshiro_stamp_list.html", {"stamps": stamps})




class OshiroStampUpdateSuccessView(LoginRequiredMixin,TemplateView):
    template_name = "oshiro_stamp_update_success.html"



class OshiroStampUpdateView(AdminOshiroRequiredMixin,LoginRequiredMixin,View):
    """お城スタンプ更新"""

    def get(self, request, stamp_id):
        stamp = _get_or_404(OshiroStampInfo, id=stamp_id)
        oshiro_list = OshiroInfo.objects.order_by("id")
        return render(request, "oshiro_stamp_update.html", {
            "stamp": stamp,
            "oshiro_list": oshiro_list
        })

    def post(self, request, stamp_id):
        if request.POST.get("cancel"):
            return redirect("admin_oshiro_stamp:oshiro_stamp_list")

        stamp = _get_or_404(OshiroStampInfo, id=stamp_id)

        stamp_name = request.POST.get("stamp_name")
        stamp_image = request.FILES.get("stamp_image")

        # 3. バリデーション
        if not stamp_name:
            return render(request, "oshiro_stamp_update.html", {
                "stamp": stamp,
                "oshiro": stamp.oshiro_info,
                "error": "スタンプ名は必須項目です"
            })
        stamp.stamp_name = stamp_name
        if stamp_image:
            stamp.oshiro_stamp_image = stamp_image
        stamp.save()

        return redirect("admin_oshiro_stamp:oshiro_stamp_update_success")

