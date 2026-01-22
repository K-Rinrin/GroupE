from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from operator_oshiro_info.models import OshiroInfo
from django.db.models import Avg,Count
from admin_model_course.models import ModelCourse, CourseReview


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
            queryset = ModelCourse.objects.filter(oshiro_info=oshiro).annotate(
                review_count=Count('reviews')
            )
            
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
            # courseから oshiro_info も辿れるようにしておく
            course = get_object_or_404(ModelCourse.objects.select_related('oshiro_info').prefetch_related('spots'), pk=pk)
            context['course'] = course
            
            if self.request.user.is_authenticated:
                my_review = CourseReview.objects.filter(
                    model_course=course, 
                    user=self.request.user
                ).first()
                context['my_review'] = my_review
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account') 

        pk = request.POST.get('course_id')
        try:
            rating = int(request.POST.get('rating'))
        except (ValueError, TypeError):
            return redirect(f"{request.path}?pk={pk}")

        course = get_object_or_404(ModelCourse, pk=pk)

        # ★重要: update_or_create を使うことで重複を防ぐ
        CourseReview.objects.update_or_create(
            model_course=course,
            user=request.user,
            defaults={'rating': rating}
        )

        # 平均点の更新
        avg = course.reviews.aggregate(Avg('rating'))['rating__avg']
        course.five_star_review = round(avg, 1) if avg else 0
        course.save()

        return redirect(f"{request.path}?pk={pk}")