# admin_area_map/forms.py
from django import forms
from .models import AreaMapInfo

ICON_CHOICES = [
    ("QR", "QR"),
    ("トイレ", "トイレ"),
    ("見どころポイント", "見どころポイント"),
    ("バリアフリー情報", "バリアフリー情報"),
]

class AreaMapInfoForm(forms.ModelForm):
    icon_name = forms.ChoiceField(choices=ICON_CHOICES)

    class Meta:
        model = AreaMapInfo
        fields = ["icon_name", "icon_image", "latitude", "longitude"]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
