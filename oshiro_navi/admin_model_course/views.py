from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# モデルのインポート
from .models import ModelCourse, ModelCourseSpot
from operator_oshiro_info.models import OshiroInfo

try:
    from admin_accounts.models import Admin
except ImportError:
    pass


# ---------------------------------------------------------
# 1. お城選択画面
# ---------------------------------------------------------
class ModelCouseSearchView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_search.html"

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


# ---------------------------------------------------------
# 2. 一覧画面
# ---------------------------------------------------------
class ModelCouseListView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        oshiro = get_object_or_404(OshiroInfo, pk=oshiro_id)
        
        queryset = ModelCourse.objects.filter(oshiro_info=oshiro)

        difficulty_filter = self.request.GET.get('difficulty')
        if difficulty_filter:
            queryset = queryset.filter(difficulty=difficulty_filter)
        
        context['oshiro'] = oshiro
        context['rows'] = queryset
        context['current_difficulty'] = difficulty_filter
        
        return context


# ---------------------------------------------------------
# 3. 新規登録 (Registar)
# ---------------------------------------------------------
class ModelCouseRegistarView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context

    def post(self, request, *args, **kwargs):
        # 新規登録は oshiro_id を使う
        oshiro_id = self.kwargs.get('oshiro_id')
        oshiro = get_object_or_404(OshiroInfo, pk=oshiro_id)
        user = request.user

        try:
            data = request.POST
            files = request.FILES
            admin_obj = Admin.objects.get(account=user)

            # 1. 親（コース）の新規作成
            course = ModelCourse.objects.create(
                oshiro_info=oshiro,
                admin=admin_obj,
                model_course_name=data.get('course_name'),
                course_overview=data.get('course_overview'),
                required_time=data.get('required_time'),
                distance=data.get('distance'),
                difficulty=data.get('difficulty'),
                five_star_review=0
            )

            # 2. 子（スポット）の作成
            for i in range(1, 31):
                name_key = f'spot_name_{i}'
                if data.get(name_key):
                    ModelCourseSpot.objects.create(
                        model_course=course,
                        order=i,
                        name=data.get(f'spot_name_{i}'),
                        short_description=data.get(f'spot_short_{i}'),
                        detail=data.get(f'spot_detail_{i}'),
                        image=files.get(f'spot_image_{i}'),
                        note=data.get(f'spot_note_{i}')
                    )

            return redirect('admin_model_course:model_couse_registar_success', oshiro_id=oshiro.pk)
            
        except Exception as e:
            print(f"登録エラー: {e}")
            context = self.get_context_data(**kwargs)
            context['error_message'] = f"エラー: {e}"
            return render(request, self.template_name, context)


# ---------------------------------------------------------
# 4. 登録完了
# ---------------------------------------------------------
class ModelCouseRegistarSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context


# ---------------------------------------------------------
# 5. 編集（更新） (Update)
# ---------------------------------------------------------
class ModelCouseUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        
        course = get_object_or_404(ModelCourse, pk=pk)
        
        context['course'] = course
        context['oshiro'] = course.oshiro_info
        context['spots'] = course.spots.all().order_by('order')
        return context

    def post(self, request, *args, **kwargs):
        # 更新は pk (コースID) を使う
        pk = self.kwargs.get('pk')
        course = get_object_or_404(ModelCourse, pk=pk)
        
        try:
            data = request.POST
            files = request.FILES

            # 1. 親情報の更新
            course.model_course_name = data.get('course_name')
            course.course_overview = data.get('course_overview')
            course.required_time = data.get('required_time')
            course.distance = data.get('distance')
            course.difficulty = data.get('difficulty')
            course.save()

            # ▼▼▼ 修正箇所：既存の画像を退避しておく ▼▼▼
            existing_images = {}
            for spot in course.spots.all():
                if spot.image:
                    existing_images[spot.order] = spot.image

            # 2. 子情報の更新（一度全消し）
            course.spots.all().delete()

            # 3. 再作成
            for i in range(1, 31):
                name_key = f'spot_name_{i}'
                
                # 名前がある場合のみ保存
                if data.get(name_key):
                    # 画像の決定ロジック
                    image_to_save = files.get(f'spot_image_{i}')
                    
                    # 新しい画像がなく、かつ古い画像があればそれを引き継ぐ
                    if not image_to_save and i in existing_images:
                        image_to_save = existing_images[i]

                    ModelCourseSpot.objects.create(
                        model_course=course,
                        order=i,
                        name=data.get(f'spot_name_{i}'),
                        short_description=data.get(f'spot_short_{i}'),
                        detail=data.get(f'spot_detail_{i}'),
                        image=image_to_save,  # 設定した画像を保存
                        note=data.get(f'spot_note_{i}')
                    )

            return redirect('admin_model_course:model_couse_update_success', oshiro_id=course.oshiro_info.pk)

        except Exception as e:
            print(f"更新エラー: {e}")
            context = self.get_context_data(**kwargs)
            context['error_message'] = "更新中にエラーが発生しました。"
            return render(request, self.template_name, context)


# ---------------------------------------------------------
# 6. 編集完了
# ---------------------------------------------------------
class ModelCouseUpdateSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context