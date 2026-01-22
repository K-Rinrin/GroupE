from django import forms
from user_accounts.models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview  # これが抜けているか、インデントがずれるとエラーになります
        fields = ['review_title', 'five_star_review', 'review_comments', 'review_image']
        
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-control'}),
            'review_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'review_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'five_star_review': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. 必須設定の強制
        self.fields['review_title'].required = True
        self.fields['review_comments'].required = True
        self.fields['five_star_review'].required = True
        self.fields['review_image'].required = False  # 画像だけ任意

        # 2. 指定されたエラーメッセージのセット
        self.fields['review_title'].error_messages = {'required': 'タイトルが未入力です'}
        self.fields['review_comments'].error_messages = {'required': 'コメントが未入力です'}
        self.fields['five_star_review'].error_messages = {'required': '評価が未入力です'}

        # 3. ブラウザ標準の吹き出しを無効化（HTML5のバリデーションを回避）
        for field in self.fields.values():
            field.widget.attrs.pop('required', None)