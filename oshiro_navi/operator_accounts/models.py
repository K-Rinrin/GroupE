import math
from django.db import models
from django.conf import settings 

class Operator(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="operator_profile",
        help_text="運営としてのアカウント"
    )

    class Meta:
        db_table = "operator"
        verbose_name = "運営"
        verbose_name_plural = "運営"

    def __str__(self):
        return f"Operator({self.account.username})"
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        2点の緯度経度から距離（メートル）を計算する（ハバーシン公式）
        """
        R = 6371000  # 地球の半径（メートル）
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # ここから下の計算も関数の中にインデントする必要があります
        a = math.sin(delta_phi / 2)**2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c  # 距離（m）を返す