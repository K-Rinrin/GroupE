from django import forms
from django.contrib.auth import get_user_model
from admin_accounts.models import Admin # 作成対象のモデルをインポート
from operator_oshiro_info.models import OshiroInfo

User = get_user_model()

class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)

    # 担当するお城を選択するフィールドを追加
    # ManyToManyFieldの場合は ModelMultipleChoiceField を使用します
    managed_castles = forms.ModelMultipleChoiceField(
        queryset=OshiroInfo.objects.all(),
        label="担当するお城",
        widget=forms.CheckboxSelectMultiple, # チェックボックス形式で選択
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_managed_castles(self):
        castles = self.cleaned_data.get('managed_castles')
        if castles and castles.count() > 5:
            raise forms.ValidationError("管理できるお城は最大5つまでです。")
        return castles
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True # 管理者なのでスタッフ権限付与
        if commit:
            user.save()
            # ここで別アプリの Admin を生成
            admin_profile = Admin.objects.create(account=user)

            # 選択されたお城をリスト化して、1つずつフィールドに割り当てる
            castles = list(self.cleaned_data.get('managed_castles', []))
            
            # 安全に値をセットするためのループ処理
            if len(castles) >= 1: Admin.oshiro_management1 = castles[0]
            if len(castles) >= 2: Admin.oshiro_management2 = castles[1]
            if len(castles) >= 3: Admin.oshiro_management3 = castles[2]
            if len(castles) >= 4: Admin.oshiro_management4 = castles[3]
            if len(castles) >= 5: Admin.oshiro_management5 = castles[4]
            
            admin_profile.save()
        return user