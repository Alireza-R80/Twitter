from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from users.tasks import send_mail_func
from .serializers import TweetSerializer
from .models import Tweet
from .utils import send_post_update_to_followers
from . import elastic


class TweetsView(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        tweet = serializer.save(user=user)
        elastic.create_tweet(tweet)
        tweet_data =serializer.data
        send_post_update_to_followers(user.followers.all(), tweet_data)

    def perform_update(self, serializer):
        instance = serializer.save()
        elastic.update_tweet(instance)

    def perform_destroy(self, instance):
        elastic.delete_tweet(instance)
        return super().perform_destroy(instance)

class FollowingTweets(ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(user__in=user.followings.all())


class SendMailToAll(APIView):
    def post(self, request):
        top_retweeted_tweet = (
            Tweet.objects.annotate(n=Count("retweets")).order_by("-n").first()
        )
        title = "top retweeted tweet"
        message = top_retweeted_tweet.content
        send_mail_func.delay(title, message)
        response = {"detail": "Sent Email Successfully...Check your mail please"}
        return Response(response)
