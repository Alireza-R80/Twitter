from elasticsearch_dsl import Document, Text, Date, Search
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
import json


class TweetSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField()


class TweetIndex(Document):
    content = Text()
    created_at = Date()

    class Index:
        name = "tweets"


def create_tweet(instance):
    tweet_index = TweetIndex()
    tweet_index.content = instance.content
    tweet_index.created_at = instance.created_at
    tweet_index.save()


def update_tweet(instance):
    tweet_index = TweetIndex.get(id=instance.id)
    tweet_index.content = instance.content
    tweet_index.save()


def delete_tweet(instance):
    tweet_index = TweetIndex.get(id=instance.id)
    tweet_index.delete()


# def search_tweets(request):
#     query = request.GET.get("q", "")
#     s = Search(index="tweets").query("match", content=query)
#     response = s.execute()

#     data = TweetSerializer(response.hits, many=True).data
#     print(data)
#     return Response(data=json.dumps(data), status=status.HTTP_200_OK)

class SearchTweetsAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        s = Search(index="tweets").query("wildcard", content=f"*{query}*")
        response = s.execute()

        data = TweetSerializer(response.hits, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)