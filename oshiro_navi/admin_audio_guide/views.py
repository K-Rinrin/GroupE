from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class AudioGuideListtView(TemplateView):
    template_name = "audio_guide_list.html"

# 登録画面
class AudioGuideRegistarView(TemplateView):
    template_name = "audio_guide_registar.html"

# 登録完了画面
class AudioGuideRegistarSuccessView(TemplateView):
    template_name = "audio_guide_registar_success.html"



# 更新画面
class AudioGuideUpdateView(TemplateView):
    template_name = "audio_guide_update.html"

# 更新完了画面
class AudioGuideUpdateSuccessView(TemplateView):
    template_name = "audio_guide_update_success.html"



# 削除画面
class AudioGuideDeleteView(TemplateView):
    template_name = "audio_guide_delete.html"

# 削除完了画面
class AudioGuideDeleteSuccessView(TemplateView):
    template_name = "audio_guide_delete_success.html"


# QRコード画面
class QRcodeGeneretorView(TemplateView):
    template_name = "qr_generetor.html"