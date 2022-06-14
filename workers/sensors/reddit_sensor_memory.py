import datetime
import sys
import warnings

# Import the libraries
import numpy as np
import pandas as pd

from cog_mem_api.MemoryContent import MemoryContent
from workers.sensors.sensory_memory import Sensor

warnings.simplefilter(action='ignore', category=FutureWarning)
sys.setrecursionlimit(1500)
import pytz
from langdetect import detect

utc = pytz.UTC

# newapi library
# youtube api libraries

# Data Preprocessing and Feature Engineering
from textblob import TextBlob
import string

# reddit libraries
import praw


class RedditSensor(Sensor):
    def __init__(self):
        super().__init__(name="REDDIT", internal_id="REDDIT", interval=86400, attention_limit=1000, source="REDDIT")
        self.reddit = praw.Reddit(client_id='9HwE8uvXZeJhVc8yQg7ISQ',
                                  client_secret='LdgRC8E7u8CfnRAU7Ymb06l73aolmg',
                                  user_agent='Muhammad Waheed Waqar')

    def localize_date(self, date):
        return utc.localize(date)

    def Start(self, instances: list):
        for record in instances:
            df = self.FetchSensorData(record['keyword'])

            if df.shape[0] == 0:
                continue
            else:
                temp = np.datetime64(record['scrapped_at'])
                latest = df[df['date'] > temp]
                senti_df = self.DoLowLevelPerception(latest)
                self.AddMemory(senti_df)

    def FetchSensorData(self, keyword) -> pd.DataFrame:
        posts = []
        keyword = str(keyword).lower()
        # scrapped data from reddit using reddit api
        for post in self.reddit.subreddit("all").search(keyword):
            date_type = type(post.created)
            date = datetime.datetime.fromtimestamp(int(post.created)).strftime('%Y-%m-%d %H:%M:%S') \
                if date_type == int or date_type == float else post.created
            record = {"id": str(post.id).encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'),
                      'url': str(post.url).encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'),
                      'title': str(post.title).encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'),
                      'body': str(post.selftext).encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'),
                      'date': date,
                      'num_comments': str(post.num_comments).encode('utf-8', 'surrogateescape').decode('utf-8',
                                                                                                       'replace'),
                      'score': post.score,
                      'upvote_ratio': post.upvote_ratio,
                      'ups': post.ups, 'downs': post.downs,
                      'keyword': keyword}
            posts.append(record)
        df = pd.DataFrame(posts)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['date'].apply(self.localize_date)

        return df

    def live_data_response(self, keyword, source) -> bool:
        return super().live_data_response(keyword, source)

    def AddMemory(self, memory_content: pd.DataFrame, source="REDDIT"):
        super().AddMemory(memory_content, source)

    def RemoveMemory(self, cue):
        pass

    def dataCleaning(self, text):
        from nltk.corpus import stopwords
        punctuation = string.punctuation
        stopwords = stopwords.words('english')
        text = text.lower()
        text = "".join(x for x in text if x not in punctuation)
        words = text.split()
        words = [w for w in words if w not in stopwords]
        text = " ".join(words)

        return text

    def detect_language(self, text):
        try:
            lang = detect(text)
        except:
            try:
                lang = TextBlob(text).detect_language()
            except:
                lang = "None"
        return lang

    def DoLowLevelPerception(self, posts: pd.DataFrame) -> pd.DataFrame:

        if posts.shape[0] == 0:
            return posts

        # Clean title and make another column to store cleaned title
        posts['title'] = posts['title'].apply(self.dataCleaning)

        # calculate polarity and subjectivity of title using textblob
        posts['polarity'] = posts['title'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)
        posts['subjectivity'] = posts['title'].apply(lambda tweet: TextBlob(tweet).sentiment.subjectivity)
        posts['language'] = posts['title'].apply(self.detect_language)
        # posts['language'] = posts['title'].apply(lambda x: TextBlob(x).detect_language())

        return posts


reddit_sensor = RedditSensor()

if __name__ == '__main__':
    pass
