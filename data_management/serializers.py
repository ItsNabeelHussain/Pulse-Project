from rest_framework import serializers
from .models import *


class NEWSSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # fields = ['source', 'title', 'description', 'url', 'polarity', 'subjectivity', 'publishedat']  # '__all__'
        fields = '__all__'


class REDDITSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reddit
        # fields = ['url', 'title', 'body', 'date', 'polarity', 'subjectivity']  # '__all__'
        fields = '__all__'


class TwitterSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twitter
        # fields = ['tweet', 'link', 'published_at', 'likes_count', 'name', 'polarity', 'subjectivity']  # '__all__'
        fields = '__all__'


class YouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = '__all__'
        # ['title', 'published_date', 'description', 'views', 'polarity', 'subjectivity', 'comment_count',
        # 'disliked', 'liked']  # '__all__ '
