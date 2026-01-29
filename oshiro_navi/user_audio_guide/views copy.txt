from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from operator_oshiro_info.models import OshiroInfo
from admin_audio_guide.models import AudioGuide
from django.shortcuts import get_object_or_404


# Create your views here.
# ユーザー側：音声ガイドお城一覧画面
class UserAudioGuideOshiroListView(TemplateView):
    template_name = "user_audio_guide_oshiro_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = OshiroInfo.objects.all()
        return context

# ユーザー側：音声ガイド一覧画面
class UserAudioGuideListView(TemplateView):
    template_name = "user_audio_guide_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # URLから渡された oshiro_id を取得
        oshiro_id = self.kwargs.get('oshiro_id')
        
        # そのIDに基づいてお城と音声ガイドを取得
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        context['oshiro'] = oshiro
        context['rows'] = AudioGuide.objects.filter(oshiro_info=oshiro).order_by("id")
        
        return context


# ユーザー側：音声ガイド用：QRスキャン画面
class QrScanView(TemplateView):
    template_name = "qr_scan.html"