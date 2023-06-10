from django.urls import path, include
from rest_framework import routers
from .elastic import SearchTweetsAPIView
from .views import TweetsView, FollowingTweets, SendMailToAll

router = routers.DefaultRouter()
router.register('tweet', TweetsView)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', SearchTweetsAPIView.as_view(), name='search_tweets'),
    path('following_tweets/', FollowingTweets.as_view(), name='followings_tweets'),
    path('send_mail/', SendMailToAll.as_view(), name='mail'),
]
