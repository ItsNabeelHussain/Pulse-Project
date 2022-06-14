from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keyword = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False, null=True)


class Configuration(models.Model):
    project = models.ForeignKey(Project, related_name='project', on_delete=models.CASCADE)
    config = models.JSONField()


class Stock(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    stock = models.ForeignKey(Stock, related_name='stock_id', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class StockClasses(models.Model):
    name = models.CharField(max_length=100)


