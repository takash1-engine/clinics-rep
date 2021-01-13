from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    age = models.IntegerField('年齢', blank=True, default=0)
    weight = models.IntegerField('体重',blank=True, default=0)