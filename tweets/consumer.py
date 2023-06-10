from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from urllib.parse import parse_qs
import json


class TweetConsumer(WebsocketConsumer):
    def connect(self):
        # Add the user to a specific WebSocket group based on their followers
        self.user = self.get_user_from_jwt()

        if self.user:
            self.followers_group_name = f"followers_{self.user.id}"
            print(self.user)
            async_to_sync(self.channel_layer.group_add)(
                self.followers_group_name, self.channel_name
            )
            self.accept()
        else:
            # Reject the connection
            self.close()


    def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        async_to_sync(self.channel_layer.group_discard)(
            self.followers_group_name, self.channel_name
        )

    def get_user_from_jwt(self):
        jwt_auth = JWTAuthentication()
        try:
            # Get the token from the headers
            query_params = parse_qs(self.scope['query_string'].decode())
            print(query_params)
            print("------------------------------------------")
            token = query_params.get('token')[0]
            print(token)
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            print(user)
            return user
        except Exception:
            return None

    def send_post_update(self, event):
        # Send the post update to the WebSocket connection
        tweet_data = json.dumps(event["text"])
        self.send(text_data=tweet_data)
