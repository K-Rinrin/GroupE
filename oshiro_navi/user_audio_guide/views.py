from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from operator_oshiro_info.models import OshiroInfo
from admin_audio_guide.models import AudioGuide
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import requests     
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
# ユーザー側：音声ガイドお城一覧画面
class UserAudioGuideOshiroListView(TemplateView):
    template_name = "user_audio_guide_oshiro_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = OshiroInfo.objects.all()
        return context



@method_decorator(csrf_exempt, name='dispatch')
class UserAudioGuideListView(TemplateView):
    template_name = "user_audio_guide_list.html"

    # --- 1. 振り分け処理 ---
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    # --- 2. 音声生成処理（ここが足りなかったか、位置がズレていたのだ！） ---
    # 必ず def dispatch と同じ高さのインデント（段落）にするのだ！
    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', '')
        speaker = request.POST.get('speaker', '3')

        if not text:
            return HttpResponse("テキストがないのだ", status=400)

        API_KEY = "Z8f9i-e-T21_388"
        API_URL = "https://api.tts.quest/v3/voicevox/synthesis"
        
        try:
            response = requests.get(API_URL, params={
                'text': text, 
                'speaker': speaker, 
                'key': API_KEY
            }, timeout=60)
            
            if response.status_code == 200:
                # 成功すればここが「audio/wav」になるのだ
                return HttpResponse(response.content, content_type="audio/wav")
            else:
                return HttpResponse(f"API Error: {response.status_code}", status=502)
        except Exception as e:
            return HttpResponse(str(e), status=500)

    # --- 3. 画面表示処理 ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        context['oshiro'] = oshiro
        context['rows'] = AudioGuide.objects.filter(oshiro_info=oshiro).order_by("id")
        return context


        
# ユーザー側：音声ガイド用：QRスキャン画面
class QrScanView(TemplateView):
    template_name = "qr_scan.html"