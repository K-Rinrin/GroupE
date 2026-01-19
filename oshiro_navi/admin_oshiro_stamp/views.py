from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404

from .models import OshiroStampInfo
from operator_oshiro_info.models import OshiroInfo  # お城情報の参照用


def _get_or_404(model_cls, **kwargs):
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")

# --- Viewクラス ---

class OshiroStampListView(View):
    """お城スタンプ一覧"""
    def get(self, request):
        try:
            # OneToOneの関係にあるお城情報もまとめて取得
            stamps = OshiroStampInfo.objects.all().select_related('oshiro_info').order_by("id")
            return render(request, "oshiro_stamp_list.html", {
                "stamps": stamps
            })
        except Exception:
            raise Http404("Unable to fetch stamp information")


class OshiroStampRegistarView(View):
    """お城スタンプ登録"""
    def get(self, request):
        # プルダウン用にお城一覧を取得
        oshiro_list = OshiroInfo.objects.all().order_by("id")
        return render(request, "oshiro_stamp_registar.html", {"oshiro_list": oshiro_list})

    def post(self, request):
        if request.POST.get("cancel"):
            return redirect("admin_oshiro_stamp:oshiro_stamp_list")

        castle_id = request.POST.get("castle_id")
        stamp_name = request.POST.get("castle_name")
        stamp_image = request.FILES.get("stamp_image")

        # バリデーション
        if not (castle_id and stamp_name and stamp_image):
            oshiro_list = OshiroInfo.objects.all().order_by("id")
            return render(request, "oshiro_stamp_registar.html", {
                "error": "必要情報を入力し、画像を選択してください",
                "oshiro_list": oshiro_list
            })

        # DB保存
        OshiroStampInfo.objects.create(
            oshiro_info_id=castle_id,
            admin=request.user,  # 現在のログインユーザー
            oshiro_stamp_image=stamp_image,
            stamp_name=stamp_name
        )

        return redirect("admin_oshiro_stamp:oshiro_stamp_registar_success")


class OshiroStampRegistarSuccessView(TemplateView):
    template_name = "oshiro_stamp_registar_success.html"
