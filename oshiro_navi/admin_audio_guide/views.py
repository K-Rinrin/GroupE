from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import AudioGuide
from django.urls import reverse
from django.views.generic.edit import UpdateView, DeleteView
from operator_oshiro_info.models import OshiroInfo  # お城情報の参照用
from admin_accounts.models import Admin  # Admin情報の参照用


# 音声ガイドお城一覧画面
class AudioGuideOshiroListView(View):
    def get(self, request):
        oshiro_list = OshiroInfo.objects.all().order_by("id")
        
        return render(
            request,
            "audio_guide_oshiro_list.html",
            {"rows": oshiro_list}
        )


# 音声ガイド一覧画面
class AudioGuideListView(View):
    def get(self, request, oshiro_id):
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        rows = (    
            AudioGuide.objects
            .filter(oshiro_info=oshiro)
            .order_by("id")
        )

        return render(
            request,
            "audio_guide_list.html",
            {
                "rows": rows,
                "oshiro": oshiro,  # oshiro.idとしてテンプレートで利用可能
            }
        )


# 登録画面
class AudioGuideRegistarView(View):
    """音声ガイド新規登録"""

    def get(self, request, oshiro_id):
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        return render(
            request,
            "audio_guide_registar.html",
            {"oshiro": oshiro}
        )

    def post(self, request, oshiro_id):
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        admin = get_object_or_404(Admin, account=request.user)

        title = request.POST.get("title")
        guide_explanation = request.POST.get("guide_explanation")

        if not title:
            return render(
                request,
                "audio_guide_registar.html",
                {
                    "oshiro": oshiro,
                    "error": "タイトルは必須です"
                }
            )

        AudioGuide.objects.create(
            oshiro_info=oshiro,
            admin=admin,
            title=title,
            guide_explanation=guide_explanation
        )

        # リダイレクト時に oshiro.id を渡す
        return redirect(
            "admin_audio_guide:audio_guide_registar_success",
            oshiro_id=oshiro.id
        )


# 登録完了画面
class AudioGuideRegistarSuccessView(TemplateView):
    template_name = "audio_guide_registar_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oshiro_id"] = self.kwargs["oshiro_id"]
        return context


# 更新画面
class AudioGuideUpdateView(View):
    """音声ガイド更新"""

    def get(self, request, oshiro_id, audio_guide_id):
        audio_guide = get_object_or_404(AudioGuide,id=audio_guide_id,oshiro_info_id=oshiro_id)
        return render(
            request,
            "audio_guide_update.html",
            {
                "audio_guide": audio_guide,
                "oshiro_id": oshiro_id,
            }
        )

    def post(self, request, oshiro_id, audio_guide_id):
        audio_guide = get_object_or_404(
            AudioGuide,
            id=audio_guide_id,
            oshiro_info_id=oshiro_id
        )

        audio_guide.title = request.POST.get("title")
        audio_guide.guide_explanation = request.POST.get("guide_explanation")
        audio_guide.save()

        # リダイレクト時に oshiro_id を一貫して使用
        return redirect(
            "admin_audio_guide:audio_guide_update_success",
            oshiro_id=oshiro_id,
            audio_guide_id=audio_guide.id
        )


# 更新完了画面
class AudioGuideUpdateSuccessView(TemplateView):
    template_name = "audio_guide_update_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oshiro_id"] = self.kwargs["oshiro_id"]
        context["audio_guide_id"] = self.kwargs["audio_guide_id"]
        return context


# 削除処理
class AudioGuideDeleteView(View):
    # 削除画面の表示
    def get(self, request, oshiro_id, audio_guide_id):
        audio_guide = get_object_or_404(
            AudioGuide,
            id=audio_guide_id,
            oshiro_info_id=oshiro_id
        )

        return render(
            request,
            "audio_guide_delete.html",
            {
                "audio_guide": audio_guide,
                "oshiro_id": oshiro_id,
            }
        )
    
    def post(self, request, oshiro_id, audio_guide_id):
        # 削除処理
        audio_guide = get_object_or_404(
            AudioGuide,
            id=audio_guide_id,
            oshiro_info_id=oshiro_id
        )
        
        # データベースから削除
        audio_guide.delete()
        return redirect(
            'admin_audio_guide:audio_guide_delete_success', 
            oshiro_id=oshiro_id,
            audio_guide_id=audio_guide_id
        )

# 削除完了画面
class AudioGuideDeleteSuccessView(TemplateView):
    template_name = "audio_guide_delete_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oshiro_id"] = self.kwargs["oshiro_id"]
        return context

# QRコード作成画面
class QRcodeGeneretorView(TemplateView):
    template_name = "qr_generetor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oshiro_id"] = self.kwargs.get("oshiro_id")
        return context