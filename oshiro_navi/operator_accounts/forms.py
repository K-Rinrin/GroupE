from django import forms
from django.contrib.auth import get_user_model
from admin_accounts.models import Admin
from operator_oshiro_info.models import OshiroInfo

User = get_user_model()

class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)

    managed_castles = forms.Field(
        label="担当するお城（最大5つ）",
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password','account_name']

    def clean_managed_castles(self):
        #送信されたデータが入っています
        castle_ids = self.data.getlist('managed_castles')
        
        # 数字（ID）だけを取り出し、実際にお城がDBに存在するか確認する
        valid_castles = []
        # 重複を避けるために set を使って ID を管理
        seen_ids = set()

        for cid in castle_ids:
            if cid and cid.isdigit() and cid not in seen_ids:
                try:
                    oshiro = OshiroInfo.objects.get(id=cid)
                    valid_castles.append(oshiro)
                    seen_ids.add(cid)
                except OshiroInfo.DoesNotExist:
                    continue # 存在しないIDは無視
        
        # 最大数チェック
        if len(valid_castles) > 5:
            raise forms.ValidationError("管理できるお城は最大5つまでです。")

        # お城のインスタンスのリストを返す
        return valid_castles

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True 
        
        if commit:
            user.save()
            admin_profile = Admin.objects.create(account=user)

            # clean_managed_castles が返したリストを取得
            selected_castles = self.cleaned_data.get('managed_castles', [])

            # スロットに割り当て
            if len(selected_castles) >= 1: admin_profile.oshiro_management1 = selected_castles[0]
            if len(selected_castles) >= 2: admin_profile.oshiro_management2 = selected_castles[1]
            if len(selected_castles) >= 3: admin_profile.oshiro_management3 = selected_castles[2]
            if len(selected_castles) >= 4: admin_profile.oshiro_management4 = selected_castles[3]
            if len(selected_castles) >= 5: admin_profile.oshiro_management5 = selected_castles[4]
            
            admin_profile.save()
        return user