# Schedule Library imported
from django.utils import timezone
from scheduler.models import KeywordScheduling
from workers.sensors.news_sensor_memory import news_sensor
from workers.sensors.reddit_sensor_memory import reddit_sensor
from workers.sensors.twitter_sensor_memory import twitter_sensor
from workers.sensors.youtube_sensor_memory import youtube_sensor
import apscheduler as apscheduler
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(daemon=True)

    def schedule(self):
        self.scheduler.add_job(func=self.start, trigger="interval", hours=12)
        self.scheduler.start()

    def start(self):
        keywords = KeywordScheduling.objects.all().values('keyword', 'scrapped_at')
        news_sensor.Start(keywords)
        reddit_sensor.Start(keywords)
        twitter_sensor.Start(keywords)
        youtube_sensor.Start(keywords)
        for keyword in keywords:
            KeywordScheduling.objects.filter(keyword=keyword['keyword']).update(scrapped_at=timezone.now)


schedule = Scheduler()
if __name__ == '__main__':
    schedule.schedule()
