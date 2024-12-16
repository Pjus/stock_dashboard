from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일을 고유 값으로 사용
    is_active = models.BooleanField(default=True)  # 활성화 여부
    # 추가 필드
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
