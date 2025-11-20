from django.db import models
from django.contrib.auth.models import User # Django組み込みのUserモデルを利用することも多いが、今回はUMLに基づき自作モデルを定義

# ========================================
# アカウント関連
# ========================================

class アカウント(models.Model):
    """ユーザーのアカウント基本情報"""
    Email = models.EmailField(
        verbose_name='メールアドレス',
        unique=True
    )
    # UMLではPK指定があるため、明示的に指定
    ID = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name='ID'
    )
    Pass = models.CharField(
        max_length=128, # パスワードはハッシュ化するため長めに設定
        verbose_name='パスワード'
    )
    アカウント名 = models.CharField(
        max_length=100,
        verbose_name='アカウント名'
    )

    class Meta:
        verbose_name = 'アカウント'
        verbose_name_plural = 'アカウント'

    def __str__(self):
        return self.アカウント名


class 利用者(models.Model):
    """一般利用者情報（アカウントと1対1）"""
    アカウント = models.OneToOneField(
        アカウント,
        on_delete=models.CASCADE,
        verbose_name='アカウント'
    )
    プロフィール画像 = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        verbose_name='プロフィール画像'
    )
    自己紹介 = models.TextField(
        blank=True,
        verbose_name='自己紹介'
    )

    class Meta:
        verbose_name = '利用者'
        verbose_name_plural = '利用者'

    def __str__(self):
        return f"利用者: {self.アカウント.アカウント名}"


class 管理者(models.Model):
    """お城の管理者情報（アカウントと1対1）"""
    アカウント = models.OneToOneField(
        アカウント,
        on_delete=models.CASCADE,
        verbose_name='アカウント'
    )
    # お城情報モデルとのリレーションは、ForeignKeyとして定義する
    # お城情報クラスが後で定義されるため、文字列でクラス名を指定
    管理するお城1 = models.ForeignKey(
        'お城情報',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_by_admin1',
        verbose_name='管理するお城1'
    )
    管理するお城2 = models.ForeignKey(
        'お城情報',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_by_admin2',
        verbose_name='管理するお城2'
    )
    管理するお城3 = models.ForeignKey(
        'お城情報',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_by_admin3',
        verbose_name='管理するお城3'
    )
    管理するお城4 = models.ForeignKey(
        'お城情報',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_by_admin4',
        verbose_name='管理するお城4'
    )
    管理するお城5 = models.ForeignKey(
        'お城情報',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_by_admin5',
        verbose_name='管理するお城5'
    )

    class Meta:
        verbose_name = '管理者'
        verbose_name_plural = '管理者'

    def __str__(self):
        return f"管理者: {self.アカウント.アカウント名}"


class 運営(models.Model):
    """プラットフォーム運営者情報（アカウントと1対1）"""
    アカウント = models.OneToOneField(
        アカウント,
        on_delete=models.CASCADE,
        verbose_name='アカウント'
    )

    class Meta:
        verbose_name = '運営'
        verbose_name_plural = '運営'

    def __str__(self):
        return f"運営: {self.アカウント.アカウント名}"


# ========================================
# お城情報関連
# ========================================

class お城情報(models.Model):
    """お城の基本データ"""
    お城名 = models.CharField(
        max_length=200,
        verbose_name='お城名'
    )
    お城画像 = models.ImageField(
        upload_to='castles/',
        verbose_name='お城画像'
    )
    住所 = models.CharField(
        max_length=300,
        verbose_name='住所'
    )
    築城年 = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='築城年'
    )
    構造 = models.TextField(
        blank=True,
        verbose_name='構造'
    )
    遺構 = models.TextField(
        blank=True,
        verbose_name='遺構'
    )
    
    # 運営と管理者からの参照は関連付け定義で確認できるが、ここではForeignKeyは追加しない
    # （運営/管理者からお城情報への関連は、別モデルのForeignKeyや管理者モデルのフィールドで対応済み）

    class Meta:
        verbose_name = 'お城情報'
        verbose_name_plural = 'お城情報'

    def __str__(self):
        return self.お城名


class 基本情報(models.Model):
    """お城の付帯情報（お城情報と1対1）"""
    お城情報 = models.OneToOneField(
        お城情報,
        on_delete=models.CASCADE,
        verbose_name='お城情報'
    )
    入場料 = models.IntegerField(
        default=0,
        verbose_name='入場料'
    )
    営業時間 = models.CharField(
        max_length=100,
        verbose_name='営業時間'
    ) # TimeFieldでも良いが、柔軟性を考慮しCharField/TextFieldにすることも多い
    アクセス情報 = models.TextField(
        blank=True,
        verbose_name='アクセス情報'
    )
    見どころ画像 = models.ImageField(
        upload_to='attractions/',
        null=True,
        blank=True,
        verbose_name='見どころ画像'
    )
    見どころ説明 = models.TextField(
        blank=True,
        verbose_name='見どころ説明'
    )
    御城印画像 = models.ImageField(
        upload_to='goshoin/',
        null=True,
        blank=True,
        verbose_name='御城印画像'
    )
    御城印説明 = models.TextField(
        blank=True,
        verbose_name='御城印説明'
    )
    # 周辺MAP:mapは、周辺MAP情報モデルで基本情報へのFKとして対応するためここでは不要

    class Meta:
        verbose_name = '基本情報'
        verbose_name_plural = '基本情報'

    def __str__(self):
        return f"{self.お城情報.お城名}の基本情報"


class 周辺MAP情報(models.Model):
    """周辺のスポット情報（基本情報と多対1）"""
    基本情報 = models.ForeignKey(
        基本情報,
        on_delete=models.CASCADE,
        verbose_name='基本情報'
    )
    アイコン名 = models.CharField(
        max_length=100,
        verbose_name='アイコン名'
    )
    アイコン画像 = models.ImageField(
        upload_to='maps/icons/',
        null=True,
        blank=True,
        verbose_name='アイコン画像'
    )
    緯度 = models.FloatField(
        verbose_name='緯度'
    )
    経度 = models.FloatField(
        verbose_name='経度'
    )

    class Meta:
        verbose_name = '周辺MAP情報'
        verbose_name_plural = '周辺MAP情報'

    def __str__(self):
        return f"{self.基本情報.お城情報.お城名} - {self.アイコン名}"


class 音声ガイド(models.Model):
    """お城の音声ガイド情報（お城情報と多対1）"""
    お城情報 = models.ForeignKey(
        お城情報,
        on_delete=models.CASCADE,
        verbose_name='お城情報'
    )
    タイトル = models.CharField(
        max_length=200,
        verbose_name='タイトル'
    )
    ガイド説明 = models.TextField(
        verbose_name='ガイド説明'
    )
    QR = models.ImageField(
        upload_to='audio_guide/qr/',
        verbose_name='QR画像'
    )

    class Meta:
        verbose_name = '音声ガイド'
        verbose_name_plural = '音声ガイド'

    def __str__(self):
        return f"{self.お城情報.お城名} - {self.タイトル}"


class モデルコース(models.Model):
    """お城の周遊モデルコース情報（お城情報と多対1）"""
    お城情報 = models.ForeignKey(
        お城情報,
        on_delete=models.CASCADE,
        verbose_name='お城情報'
    )
    モデルコース名 = models.CharField(
        max_length=200,
        verbose_name='モデルコース名'
    )
    距離 = models.FloatField(
        help_text='単位はkmなどを想定',
        verbose_name='距離'
    )
    所要時間 = models.CharField(
        max_length=50,
        verbose_name='所要時間'
    ) # TimeFieldでも良いが、柔軟性を考慮しChar/TextFieldにすることも多い
    コース概要 = models.TextField(
        verbose_name='コース概要'
    )
    難易度 = models.CharField(
        max_length=50,
        verbose_name='難易度'
    )
    評価 = models.FloatField(
        null=True,
        blank=True,
        verbose_name='評価'
    )

    class Meta:
        verbose_name = 'モデルコース'
        verbose_name_plural = 'モデルコース'

    def __str__(self):
        return f"{self.お城情報.お城名} - {self.モデルコース名}"


# ========================================
# イベント・口コミ関連
# ========================================

class イベント情報(models.Model):
    """お城で開催されるイベント情報"""
    運営 = models.ForeignKey(
        運営,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='運営'
    )
    管理者 = models.ForeignKey(
        管理者,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='管理者'
    )
    イベント名 = models.CharField(
        max_length=200,
        verbose_name='イベント名'
    )
    イベント概要 = models.TextField(
        verbose_name='イベント概要'
    )
    開催場所 = models.CharField(
        max_length=300,
        verbose_name='開催場所'
    )
    開催日時 = models.DateTimeField(
        verbose_name='開催日時'
    )
    公開設定 = models.BooleanField(
        default=False,
        verbose_name='公開設定'
    )

    class Meta:
        verbose_name = 'イベント情報'
        verbose_name_plural = 'イベント情報'

    def __str__(self):
        return self.イベント名


class 口コミ(models.Model):
    """利用者からのお城への口コミ"""
    利用者 = models.ForeignKey(
        利用者,
        on_delete=models.CASCADE,
        verbose_name='利用者'
    )
    タイトル = models.CharField(
        max_length=100,
        verbose_name='タイトル'
    )
    コメント = models.TextField(
        verbose_name='コメント'
    )
    写真 = models.ImageField(
        upload_to='reviews/',
        null=True,
        blank=True,
        verbose_name='写真'
    )
    評価 = models.FloatField(
        verbose_name='評価'
    )
    投稿日時 = models.DateTimeField(
        auto_now_add=True, # 初回登録時に自動設定
        verbose_name='投稿日時'
    )

    class Meta:
        verbose_name = '口コミ'
        verbose_name_plural = '口コミ'

    def __str__(self):
        return f"{self.タイトル} ({self.利用者.アカウント.アカウント名})"


class お城マイリスト(models.Model):
    """利用者のお城お気に入りリスト（多対多の関係を表現）"""
    利用者 = models.ForeignKey(
        利用者,
        on_delete=models.CASCADE,
        verbose_name='利用者'
    )
    お城情報 = models.ForeignKey(
        お城情報,
        on_delete=models.CASCADE,
        verbose_name='お城情報'
    )
    # マイリストへの追加日時などをフィールドとして追加しても良い

    class Meta:
        verbose_name = 'お城マイリスト'
        verbose_name_plural = 'お城マイリスト'
        # 利用者とお城の組み合わせはユニークであるべき
        unique_together = ('利用者', 'お城情報')

    def __str__(self):
        return f"{self.利用者.アカウント.アカウント名} のマイリスト: {self.お城情報.お城名}"


# ========================================
# スタンプ関連
# ========================================

class お城スタンプ情報(models.Model):
    """お城が持つスタンプ自体の基本情報（お城情報と1対1）"""
    お城情報 = models.OneToOneField(
        お城情報,
        on_delete=models.CASCADE,
        verbose_name='お城情報'
    )
    管理者 = models.ForeignKey(
        管理者,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='管理者'
    )
    お城スタンプ画像 = models.ImageField(
        upload_to='stamps/info/',
        verbose_name='お城スタンプ画像'
    )
    スタンプ名 = models.CharField(
        max_length=100,
        verbose_name='スタンプ名'
    )

    class Meta:
        verbose_name = 'お城スタンプ情報'
        verbose_name_plural = 'お城スタンプ情報'

    def __str__(self):
        return f"{self.お城情報.お城名} のスタンプ情報"


class お城スタンプ(models.Model):
    """利用者が獲得したスタンプ記録"""
    お城スタンプ情報 = models.ForeignKey(
        お城スタンプ情報,
        on_delete=models.CASCADE,
        verbose_name='お城スタンプ情報'
    )
    利用者 = models.ForeignKey(
        利用者,
        on_delete=models.CASCADE,
        verbose_name='利用者'
    )
    お城スタンプ数 = models.IntegerField(
        default=1,
        verbose_name='お城スタンプ数'
    )
    日付 = models.DateField(
        auto_now_add=True, # 獲得日時に自動設定
        verbose_name='日付'
    )

    class Meta:
        verbose_name = 'お城スタンプ'
        verbose_name_plural = 'お城スタンプ'
        # 1人の利用者は、1つのスタンプを1日に複数回獲得できないようにする
        # UMLには記載がないが、一般的にスタンプラリーではユニーク性を保つ
        unique_together = ('利用者', 'お城スタンプ情報', '日付')

    def __str__(self):
        return f"{self.利用者.アカウント.アカウント名} - {self.お城スタンプ情報.スタンプ名} 獲得"