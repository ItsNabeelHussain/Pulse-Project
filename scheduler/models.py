from django.db import models


# Create your models here.
from django.utils import timezone


class KeywordScheduling(models.Model):
    keyword = models.CharField(max_length=50, unique=True)
    scrapped_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
