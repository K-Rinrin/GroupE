# user_my_list/models.py
from django.db import models


class OshiroMyList(models.Model):
    """
    お城マイリストテーブル（osiro_my_list）。
    利用者がお気に入り登録したお城を管理する。
    """

    # 利用者FK
    user = models.ForeignKey(
        "user_accounts.User",
        on_delete=models.CASCADE,
        db_column="user",
        help_text="マイリストを持つ利用者"
    )

    # お城情報FK
    oshiro_info = models.ForeignKey(
        "operator_oshiro_info.OshiroInfo",
        on_delete=models.CASCADE,
        db_column="oshiro_info",
        help_text="お気に入り登録されたお城"
    )

    class Meta:
        db_table = "osiro_my_list"  # テーブル定義書の物理名

    def __str__(self) -> str:
        return f"MyList(user={self.user_id}, oshiro={self.oshiro_info_id})"
