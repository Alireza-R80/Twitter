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


class TweetsView(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        tweet =serializer.data
        send_post_update_to_followers(user.followers.all(), tweet)


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
        send_mail_func.delay()
        response = {"detail": "Sent Email Successfully...Check your mail please"}
        return Response(response)
