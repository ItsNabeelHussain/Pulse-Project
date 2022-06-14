import numpy as np
import pandas as pd
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import spellchecker
from core.models import Project, Stock, Keyword, StockClasses
from .serializers import ProjectSerializer, ConfigSerializer, StockSerializer, KeywordSerializer, SCSerializer
from rest_framework import generics
from data_management.models import *
from data_management.serializers import *
from workers.sensors.news_sensor_memory import news_sensor
from workers.sensors.reddit_sensor_memory import reddit_sensor

from workers.sensors.twitter_sensor_memory import twitter_sensor
from workers.sensors.youtube_sensor_memory import youtube_sensor

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import threading
from scheduler.models import KeywordScheduling
from scheduler.schedule import schedule

spell = spellchecker.SpellChecker()
schedule.schedule()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        # Add custom claims
        token['name'] = "{0} {1}".format(user.first_name, user.last_name)
        token['email'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectList(generics.ListAPIView):
    """
              ProjectList Class

              This view performs  operation for ProjectList object

              Parameters
              ----------
              ListAPIView : rest_framework.views

              """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            projects = Project.objects.filter(user=request.user.id)  # filter(user=request.user.id)
            serializer = ProjectSerializer(projects, many=True)
            return Response({"result": serializer.data, "message": "all list"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectView(APIView):
    """
                ProjectView Class

                This view performs PUT,POST,GET,DELETE  operation for Project object

                Parameters
                ----------
                APIView : rest_framework.views

                """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns Project object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
                returns HTTP 200 status if data returned successfully,
            """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response({"result": serializer.data, "message": "project fetched"}, status=status.HTTP_200_OK)

    def post(self, request):
        """
                HTTP POST request

                An HTTP endpoint that saves a Project object in DB

                Parameters
                ----------
                request : django.http.request

                Returns
                -------
                rest_framework.response
                    returns success message if data saved successfully,error message otherwise
                """

        try:
            data = request.data
            if Project.objects.filter(keyword=data["keyword"]).count() == 0:
                keyword = data["keyword"]
                keyword_scheduling = KeywordScheduling(keyword=data["keyword"])
                keyword_scheduling.save()
                news_thread = threading.Thread(target=news_sensor.live_data_response, args=(keyword, "NEWS"))
                news_thread.start()
                reddit_thread = threading.Thread(target=reddit_sensor.live_data_response, args=(keyword, "REDDIT"))
                reddit_thread.start()
                twitter_thread = threading.Thread(target=twitter_sensor.live_data_response(keyword, "TWITTER"))
                twitter_thread.start()
                youtube_thread = threading.Thread(target=youtube_sensor.live_data_response,
                                                  args=(keyword, "YOUTUBE"))
                youtube_thread.start()
            data["user"] = request.user.id  # User.objects.get(pk=)
            serializer = ProjectSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"result": serializer.data, "message": "record created successfully"},
                                status=status.HTTP_200_OK)
            else:
                error = "{1}:{0}".format(list(serializer.errors.values())[0][0], list(serializer.errors.keys())[0])
                return Response({"details": error},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """
                HTTP PUT request

                An HTTP endpoint that updates a Project object for provided PK

                Parameters
                ----------
                request : django.http.request

                pk : integer

                Returns
                -------
                rest_framework.response
                    returns success message if data updated successfully,error message otherwise
                """

        try:
            Project.objects.filter(user=request.user.id).update(is_default=False)
            Project.objects.filter(user=request.user.id, id=pk).update(is_default=True)
            project = Project.objects.filter(id=pk)
            data = ProjectSerializer(project, many=True)
            return Response({"result": data.data[0], "message": "update default project successfully"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
               HTTP DELETE request

               An HTTP endpoint that deletes a Project object for provided PK

               Parameters
               ----------
               request : django.http.request

               pk : integer

               Returns
               -------
               rest_framework.response
                   returns success message if data deleted successfully,error message otherwise
               """
        try:
            project = self.get_object(pk)
            project.delete()
            return Response({"message": "project deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404


class Home(APIView):
    """
                Home Class

                This view performs Get operation for Home object

                Parameters
                ----------
                APIView : rest_framework.views

                """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns Home object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
                returns HTTP 200 status if data returned successfully,error message otherwise
            """
        try:
            global reddit_date, youtube_date, news_date, twitter_date, uni_reddit, uni_twitter, uni_youtube, uni_news
            uni_reddit = set()
            uni_twitter = set()
            uni_youtube = set()
            uni_news = set()
            reddit_date = pd.DataFrame()
            youtube_date = pd.DataFrame()
            news_date = pd.DataFrame()
            twitter_date = pd.DataFrame()
            reddit_thread = None
            youtube_thread = None
            news_thread = None
            twitter_thread = None
            project = None
            try:
                project = Project.objects.get(pk=pk)
            except Project.DoesNotExist:
                raise Http404
            keyword = project.keyword.lower()
            news = News.objects.using('data').filter(keyword=keyword).order_by('-publishedat')[:500]
            # print("count : ", news.count())
            # return Response(NEWSSerializer(news, many=True).data)
            if news.count() == 0:
                try:
                    news_thread = threading.Thread(target=news_sensor.live_data_response, args=(keyword, "NEWS"))
                    news_thread.start()
                except Exception as e:
                    print("Error : ", e)
            reddit = Reddit.objects.using('data').filter(keyword=keyword).order_by('-date')[:500]
            if reddit.count() == 0:
                try:
                    reddit_thread = threading.Thread(target=reddit_sensor.live_data_response, args=(keyword, "REDDIT"))
                    reddit_thread.start()
                except:
                    print("Error : ", e)
            twitter = Twitter.objects.using('data').filter(keyword=keyword).order_by('-date')[:500]
            if twitter.count() == 0:
                try:
                    twitter_thread = threading.Thread(target=twitter_sensor.live_data_response(keyword, "TWITTER"))
                    twitter_thread.start()
                except:
                    print("Error : ", e)
            youtube = Youtube.objects.using('data').filter(keyword=keyword).order_by('-published_date')[:500]
            print("youtube.count()", youtube.count())
            if youtube.count() == 0:
                try:
                    youtube_thread = threading.Thread(target=youtube_sensor.live_data_response,
                                                      args=(keyword, "YOUTUBE"))
                    youtube_thread.start()
                except:
                    print("Error : ", e)
            if news.count() == 0:
                news_thread.join()
            if youtube.count() == 0:
                youtube_thread.join()
            if twitter.count() == 0:
                twitter_thread.join()
            if youtube.count() == 0:
                youtube_thread.join()
            news = news if news.count() > 0 else News.objects.using('data').filter(keyword=keyword).order_by(
                '-publishedat')[:500]
            reddit = reddit if reddit.count() > 0 else Reddit.objects.using('data').filter(keyword=keyword).order_by(
                '-date')[:500]
            twitter = twitter if twitter.count() > 0 else Twitter.objects.using('data').filter(
                keyword=keyword).order_by('-date')[:500]
            youtube = youtube if youtube.count() > 0 else Youtube.objects.using('data').filter(
                keyword=keyword).order_by('-published_date')[:5000]

            positive_sentiments_youtube = 0
            negative_sentiments_youtube = 0
            neutral_sentiments_youtube = 0
            youtube_data = YouTubeSerializer(youtube, many=True).data
            youtube_count = len(youtube_data)
            youtube_df = pd.DataFrame(youtube_data)
            if youtube_df.shape[0] != 0:
                positive_sentiments_youtube = len(youtube_df[youtube_df.polarity > 0])
                negative_sentiments_youtube = len(youtube_df[youtube_df.polarity < 0])
                neutral_sentiments_youtube = len(youtube_df[youtube_df.polarity == 0])
                youtube_df["published_date"] = pd.to_datetime(youtube_df["published_date"]).dt.date
                youtube_date = youtube_df[["published_date", "views"]].groupby('published_date').count()

            # news
            news_data = NEWSSerializer(news, many=True).data
            positive_sentiments_news = 0
            negative_sentiments_news = 0
            neutral_sentiments_news = 0
            news_count = len(news_data)
            news_df = pd.DataFrame(news_data)
            if news_df.shape[0] != 0:
                positive_sentiments_news = len(news_df[news_df.polarity > 0])
                negative_sentiments_news = len(news_df[news_df.polarity < 0])
                neutral_sentiments_news = len(news_df[news_df.polarity == 0])
                news_df["publishedat"] = pd.to_datetime(news_df["publishedat"]).dt.date
                news_date = news_df[["publishedat", "source"]].groupby('publishedat').count()

            # Twitter
            positive_sentiments_twitter = 0
            negative_sentiments_twitter = 0
            neutral_sentiments_twitter = 0

            twitter_data = TwitterSSerializer(twitter, many=True).data
            twitter_count = len(twitter_data)
            twitter_df = pd.DataFrame(twitter_data)
            if twitter_df.shape[0] != 0:
                positive_sentiments_twitter = len(twitter_df[twitter_df["polarity"] > 0])
                negative_sentiments_twitter = len(twitter_df[twitter_df["polarity"] < 0])
                neutral_sentiments_twitter = len(twitter_df[twitter_df["polarity"] == 0])
                twitter_df["date"] = pd.to_datetime(twitter_df["date"]).dt.date
                twitter_date = twitter_df[["date", "tweet"]].groupby('date').count()

            # reddit
            positive_sentiments_reddit = 0
            negative_sentiments_reddit = 0
            neutral_sentiments_reddit = 0
            reddit_data = REDDITSerializer(reddit, many=True).data
            print("reddit_data : ", reddit_data)
            reddit_count = len(reddit_data)
            reddit_df = pd.DataFrame(reddit_data)
            if not reddit_df.empty:
                print("reddit columns : ", reddit_df.columns)
                positive_sentiments_reddit = len(reddit_df[reddit_df.polarity > 0])
                negative_sentiments_reddit = len(reddit_df[reddit_df.polarity < 0])
                neutral_sentiments_reddit = len(reddit_df[reddit_df.polarity == 0])
                reddit_df["date"] = pd.to_datetime(reddit_df["date"]).dt.date
                reddit_date = reddit_df[["date", "body"]].groupby('date').count()
            #
            positive_sentiment = positive_sentiments_twitter + positive_sentiments_reddit + positive_sentiments_news + positive_sentiments_youtube
            #
            negative_sentiment = negative_sentiments_twitter + negative_sentiments_reddit + negative_sentiments_news + negative_sentiments_youtube
            #
            neutral_sentiment = neutral_sentiments_twitter + neutral_sentiments_reddit + neutral_sentiments_news + neutral_sentiments_youtube
            total_posts = youtube_count + reddit_count + news_count + twitter_count
            visualizer = pd.concat([youtube_date, reddit_date, news_date, twitter_date], ignore_index=False)
            visualizer.fillna(value=0, inplace=True)
            print(visualizer.columns)
            print(visualizer.head())
            ''' this part is used to implement language based filter'''
            # if not reddit_df.empty:
            #     uni_reddit = set(reddit_df.language.unique())
            # if not twitter_df.empty:
            #     uni_twitter = set(twitter_df.language.unique())
            # if not youtube_df.empty:
            #     uni_youtube = set(youtube_df.language.unique())
            # if not news_df.empty:
            #     uni_news = set(news_df.language.unique())
            # language = uni_reddit.union(uni_twitter).union(uni_youtube).union(uni_news)
            ''' ended '''
            lineGraph = {
                "label": [x.strftime("%y-%m-%d") for x in list(visualizer.index)],
                "reddit": visualizer.body.to_list() if not reddit_df.empty else np.zeros(visualizer.shape[0]),
                "twitter": visualizer.tweet.to_list() if not twitter_df.empty else np.zeros(visualizer.shape[0]),
                "youtube": visualizer.views.to_list() if not youtube_df.empty else np.zeros(visualizer.shape[0]),
                "news": visualizer.source.to_list() if not news_df.empty else np.zeros(visualizer.shape[0])
            }
            response = {"cards": {
                "reddit": reddit_data,
                "twitter": twitter_data,
                "youtube": youtube_data,
                "news": news_data
            },
                "posts": {
                    "reddit": reddit_count,
                    "twitter": twitter_count,
                    "youtube": youtube_count,
                    "news": news_count
                },
                "sentiment": {
                    "positive sentiment": positive_sentiment,
                    "negative sentiment": negative_sentiment,
                    "neutral sentiment": neutral_sentiment,
                    "total posts": total_posts,
                    "twitter":
                        {
                            "positive": positive_sentiments_twitter,
                            "negative": negative_sentiments_twitter,
                            "neutral": neutral_sentiments_twitter,
                        },
                    "youtube":
                        {
                            "positive": positive_sentiments_youtube,
                            "negative": negative_sentiments_youtube,
                            "neutral": neutral_sentiments_youtube,
                        },
                    "news":
                        {
                            "positive": positive_sentiments_news,
                            "negative": negative_sentiments_news,
                            "neutral": neutral_sentiments_news,
                        },
                    "reddit":
                        {
                            "positive": positive_sentiments_reddit,
                            "negative": negative_sentiments_reddit,
                            "neutral": neutral_sentiments_reddit,
                        }
                },
                "lineGraph": lineGraph,
                # "language": list(language) language filter

            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockView(generics.ListAPIView):
    """
                StockView Class

                This view performs  operation for Stock object

                Parameters
                ----------
                ListAPIView : rest_framework.views

                """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
                  HTTP LIST request

                  An HTTP endpoint that returns all StockClasses object

                  Parameters
                  ----------
                  request : django.http.request



                  Returns
                  ---------
                  rest_framework.response
                      returns HTTP 200 status if data returned successfully,
                  """
        try:
            if not 'keyword' in list(kwargs.keys()):
                return Response({"details": "please send the keyword within request"},
                                status=status.HTTP_204_NO_CONTENT)
            key = kwargs['keyword']
            stocks = Stock.objects.filter(
                id__in=Keyword.objects.filter(keyword=key).values('stock_id'))  # filter(user=request.user.id)
            serializer = StockSerializer(stocks, many=True)
            return Response({"result": serializer.data, "message": "all list of stocks"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Http404


class StockClassesView(APIView):
    """
                StockClassesView Class

                This view performs GET,POST operation for Stock object

                Parameters
                ----------
                APIView : rest_framework.views

                """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all StockClasses object

            Parameters
            ----------
            request : django.http.request



            Returns
            ---------
            rest_framework.response
                returns HTTP 200 status if data returned successfully,
            """
        classes = StockClasses.objects.all()
        classes_serializer = SCSerializer(classes, many=True)
        return Response(classes_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
       HTTP POST request

       An HTTP endpoint that POST all StockClasses object

       Parameters
       ----------
       request : django.http.request



       Returns
       ---------
       rest_framework.response
           returns HTTP 200 status if data returned successfully,400 bad request otherwise
       """
        serializer = SCSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"details": "save successfully"}, status=status.HTTP_200_OK)
        return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)