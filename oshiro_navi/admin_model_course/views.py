from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# モデルのインポート (ModelCourseSpot は削除したのでインポートしない)
from .models import ModelCourse
from operator_oshiro_info.models import OshiroInfo

try:
    from admin_accounts.models import Admin
except ImportError:
    pass

# --- 検索画面 ---
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


# --- 一覧画面 ---
class ModelCouseListView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # URLからお城IDを取得
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


# --- 新規登録 ---
class ModelCouseRegistarView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context

    def post(self, request, *args, **kwargs):
        oshiro_id = self.kwargs.get('oshiro_id')
        oshiro = get_object_or_404(OshiroInfo, pk=oshiro_id)
        user = request.user

        try:
            data = request.POST
            files = request.FILES
            admin_obj = Admin.objects.get(account=user)

            # 1つのテーブルにまとめて保存
            ModelCourse.objects.create(
                oshiro_info=oshiro,
                admin=admin_obj,
                # 基本情報
                model_course_name=data.get('course_name'),
                course_overview=data.get('course_overview'),
                required_time=data.get('required_time'),
                distance=data.get('distance'),
                difficulty=data.get('difficulty'),
                five_star_review=0,
                # スポット1
                spot1_name=data.get('spot1_name'),
                spot1_short=data.get('spot1_short'),
                spot1_detail=data.get('spot1_detail'),
                spot1_image=files.get('spot1_image'),
                spot1_note=data.get('spot1_note'),
                # スポット2
                spot2_name=data.get('spot2_name'),
                spot2_short=data.get('spot2_short'),
                spot2_detail=data.get('spot2_detail'),
                spot2_image=files.get('spot2_image'),
                spot2_note=data.get('spot2_note')
            )
            
            return redirect('admin_model_course:model_couse_registar_success', oshiro_id=oshiro.pk)
            
        except Exception as e:
            print(f"登録エラー: {e}")
            context = self.get_context_data(**kwargs)
            context['error_message'] = f"エラーが発生しました: {e}"
            return render(request, self.template_name, context)


# --- 登録完了 ---
class ModelCouseRegistarSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_registar_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context


# --- 編集（更新） ---
class ModelCouseUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update.html"

    # GET: 既存データを表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        course = get_object_or_404(ModelCourse, pk=pk)
        
        context['course'] = course
        context['oshiro'] = course.oshiro_info
        # HTML側では {{ course.spot1_name }} のように直接アクセスすればOK
        return context

    # POST: データを更新
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        course = get_object_or_404(ModelCourse, pk=pk)
        
        try:
            data = request.POST
            files = request.FILES

            # 基本情報
            course.model_course_name = data.get('course_name')
            course.course_overview = data.get('course_overview')
            course.required_time = data.get('required_time')
            course.distance = data.get('distance')
            course.difficulty = data.get('difficulty')

            # スポット1 
            course.spot1_name = data.get('spot1_name')
            course.spot1_short = data.get('spot1_short')
            course.spot1_detail = data.get('spot1_detail')
            course.spot1_note = data.get('spot1_note')
            if files.get('spot1_image'): # 画像があれば更新
                course.spot1_image = files.get('spot1_image')

            # スポット2
            course.spot2_name = data.get('spot2_name')
            course.spot2_short = data.get('spot2_short')
            course.spot2_detail = data.get('spot2_detail')
            course.spot2_note = data.get('spot2_note')
            if files.get('spot2_image'): # 画像があれば更新
                course.spot2_image = files.get('spot2_image')

            course.save()

            return redirect('admin_model_course:model_couse_update_success', oshiro_id=course.oshiro_info.pk)

        except Exception as e:
            print(f"更新エラー: {e}")
            context = self.get_context_data(**kwargs)
            context['error_message'] = "更新中にエラーが発生しました。"
            return render(request, self.template_name, context)


# --- 編集完了 ---
class ModelCouseUpdateSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "model_couse_update_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oshiro_id = self.kwargs.get('oshiro_id')
        context['oshiro'] = get_object_or_404(OshiroInfo, pk=oshiro_id)
        return context