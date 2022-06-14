# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class News(models.Model):
    source = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    urltoimage = models.TextField(db_column='urlToImage', blank=True, null=True)  # Field name made lowercase.
    publishedat = models.DateTimeField(db_column='publishedAt', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)
    cleaned = models.TextField(blank=True, null=True)
    polarity = models.FloatField(blank=True, null=True)
    subjectivity = models.FloatField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    # id = models.BigIntegerField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'NEWS'


class Reddit(models.Model):
    id = models.TextField(primary_key=True)
    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    num_comments = models.TextField(blank=True, null=True)
    score = models.BigIntegerField(blank=True, null=True)
    upvote_ratio = models.FloatField(blank=True, null=True)
    ups = models.BigIntegerField(blank=True, null=True)
    downs = models.BigIntegerField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)
    polarity = models.FloatField(blank=True, null=True)
    subjectivity = models.FloatField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'REDDIT'


class Twitter(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    tweet = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    hashtags = models.TextField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    nlikes = models.BigIntegerField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)
    polarity = models.FloatField(blank=True, null=True)
    subjectivity = models.FloatField(blank=True, null=True)
    # id = models.BigIntegerField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'TWITTER'


class Youtube(models.Model):
    title = models.TextField(blank=True, null=True)
    video_id = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    views = models.TextField(blank=True, null=True)
    liked = models.TextField(blank=True, null=True)
    disliked = models.TextField(blank=True, null=True)
    comment_count = models.TextField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)
    polarity = models.FloatField(blank=True, null=True)
    subjectivity = models.FloatField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    # id = models.BigIntegerField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'YOUTUBE'
