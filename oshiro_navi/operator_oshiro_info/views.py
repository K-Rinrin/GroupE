from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404

from .models import OshiroInfo


def _get_or_404(model_cls, **kwargs):
    """get_object_or_404 の代替（自作）"""
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")


def _safe_int(value, default=0):
    """築城年などの数値を安全にint変換"""
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


class OshiroInfoListView(View):
    """お城情報一覧"""
    def get(self, request):
        oshiros = OshiroInfo.objects.all().order_by("id")
        return render(request, "oshiro_info_list.html", {"oshiros": oshiros})


class OshiroInfoRegisterView(View):
    """お城情報登録"""
    def get(self, request):
        return render(request, "oshiro_info_register.html")

    def post(self, request):
        if request.POST.get("cancel"):
            return redirect("operator_oshiro_info:list")

        oshiro_name = request.POST.get("oshiro_name")
        address = request.POST.get("address")
        built_year_raw = request.POST.get("built_year")
        structure = request.POST.get("structure")
        ruins = request.POST.get("ruins")

        if not (oshiro_name and address and built_year_raw and structure and ruins):
            return render(request, "oshiro_info_register.html", {"error": "必要情報を入力してください"})

        built_year = _safe_int(built_year_raw, default=None)
        if built_year is None:
            return render(request, "oshiro_info_register.html", {"error": "必要情報を入力してください"})

        OshiroInfo.objects.create(
            oshiro_name=oshiro_name,
            address=address,
            built_year=built_year,
            structure=structure,
            ruins=ruins,
        )

        return redirect("operator_oshiro_info:register_success")


class OshiroInfoRegisterSuccessView(TemplateView):
    template_name = "oshiro_info_register_success.html"


class OshiroInfoUpdateView(View):
    """お城情報更新（?id= で対象指定）"""
    def get(self, request):
        oshiro_id = request.GET.get("id")
        if not oshiro_id:
            return redirect("operator_oshiro_info:list")

        oshiro = _get_or_404(OshiroInfo, id=oshiro_id)
        return render(request, "oshiro_info_update.html", {"oshiro": oshiro})

    def post(self, request):
        if request.POST.get("cancel"):
            return redirect("operator_oshiro_info:list")

        oshiro_id = request.POST.get("id")
        if not oshiro_id:
            return redirect("operator_oshiro_info:list")

        oshiro = _get_or_404(OshiroInfo, id=oshiro_id)

        oshiro_name = request.POST.get("oshiro_name")
        address = request.POST.get("address")
        built_year_raw = request.POST.get("built_year")
        structure = request.POST.get("structure")
        ruins = request.POST.get("ruins")

        if not (oshiro_name and address and built_year_raw and structure and ruins):
            return render(request, "oshiro_info_update.html", {"oshiro": oshiro, "error": "必要情報を入力してください"})

        built_year = _safe_int(built_year_raw, default=None)
        if built_year is None:
            return render(request, "oshiro_info_update.html", {"oshiro": oshiro, "error": "必要情報を入力してください"})

        oshiro.oshiro_name = oshiro_name
        oshiro.address = address
        oshiro.built_year = built_year
        oshiro.structure = structure
        oshiro.ruins = ruins
        oshiro.save()

        return redirect("operator_oshiro_info:update_success")


class OshiroInfoUpdateSuccessView(TemplateView):
    template_name = "oshiro_info_update_success.html"
