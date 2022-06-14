from django.contrib import admin
from .reddit import RedditModelAdmin
from .news import NewsModelAdmin
from .twitter import TwitterModelAdmin
from .youtube import YouTubeModelAdmin
from data_management.models import *


admin.site.register(News, NewsModelAdmin)
admin.site.register(Reddit, RedditModelAdmin)
admin.site.register(Youtube, YouTubeModelAdmin)
admin.site.register(Twitter, TwitterModelAdmin)
