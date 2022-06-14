from abc import ABC

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from core.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  # ['id', 'user_id', 'title', 'keyword', 'is_default']

        validators = [
            UniqueTogetherValidator(
                queryset=Project.objects.all(),
                fields=['user', 'title'],
                message="project name already exist"
            )
        ]


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'project', 'config']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    keyword = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Keyword
        fields = '__all__'


class SCSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockClasses
        fields = '__all__'


