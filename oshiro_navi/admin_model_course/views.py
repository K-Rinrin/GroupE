from django.shortcuts import render
from django.views.generic import TemplateView


# 一覧
class ModelCouseListView(TemplateView):
    template_name = "model_couse_list.html"


# 新規登録
class ModelCouseRegistarView(TemplateView):
    template_name = "model_couse_registar.html"


# 新規登録完了
class ModelCouseRegistarSuccessView(TemplateView):
    template_name = "model_couse_registar_success.html"


# 編集（更新）
class ModelCouseUpdateView(TemplateView):
    template_name = "model_couse_update.html"


# 編集完了
class ModelCouseUpdateSuccessView(TemplateView):
    template_name = "model_couse_update_success.html"

