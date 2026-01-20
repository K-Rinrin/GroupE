from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from operator_oshiro_info.models import OshiroInfo
from admin_model_course.models import ModelCourse


# 1. お城選択（検索）画面
class UsermodelCourseChooseView(TemplateView):
    template_name = "model_course_choose.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 全てのお城情報を取得してテンプレートへ渡す
        context['castles'] = OshiroInfo.objects.all()
        return context
    

# 2. 検索結果一覧画面
class UserModelCourseListView(TemplateView):
    template_name = "model_course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        oshiro_id = self.request.GET.get('oshiro_id')
        
        if oshiro_id:
            oshiro = get_object_or_404(OshiroInfo, pk=oshiro_id)
            queryset = ModelCourse.objects.filter(oshiro_info=oshiro)
            
            difficulty_filter = self.request.GET.get('difficulty')
            if difficulty_filter:
                queryset = queryset.filter(difficulty=difficulty_filter)
            
            context['oshiro'] = oshiro
            context['courses'] = queryset
            context['oshiro_id'] = oshiro_id 
            context['current_difficulty'] = difficulty_filter
        else:
            context['courses'] = []
            
        return context


# 3. コース詳細画面
class UserModelCourseDetailView(TemplateView):
    template_name = "model_course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.GET.get('pk')
        if pk:
            course = get_object_or_404(ModelCourse, pk=pk)
            context['course'] = course
        return context