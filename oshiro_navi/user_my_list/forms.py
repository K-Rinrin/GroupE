from django import forms
from user_accounts.models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['review_title', 'review_comments', 'five_star_review', 'review_image']
        widgets = {
            'review_title': forms.TextInput(attrs={'style': 'width: 100%; border: 1px solid #000; padding: 5px;'}),
            'review_comments': forms.Textarea(attrs={'style': 'width: 100%; border: 1px solid #000; padding: 5px;', 'rows': 4}),
            'five_star_review': forms.NumberInput(attrs={'style': 'width: 100%; border: 1px solid #000; padding: 5px;', 'min': 1, 'max': 5}), 'five_star_review': forms.RadioSelect(choices=[
                (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')
            ]),            
        }

