from django import forms
from user_accounts.models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['review_title', 'five_star_review', 'review_comments', 'review_image']
        
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-control'}),
            'review_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'review_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'five_star_review': forms.HiddenInput(), # JavaScriptで値を入れます
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 画像だけを任意（入力しなくてOK）に設定
        self.fields['review_image'].required = False
        self.fields['five_star_review'].widget.attrs.update({'min': '1', 'max': '5'})