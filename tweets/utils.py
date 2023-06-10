from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_post_update_to_followers(followers, tweet):
    channel_layer = get_channel_layer()

    # Loop over the followers and send the post update to each follower
    for follower in followers:
        print(follower.id)
        async_to_sync(channel_layer.group_send)(
            f"followers_{follower.id}",
            {
                "type": "send_post_update",
                "text": tweet,
            },
        )
