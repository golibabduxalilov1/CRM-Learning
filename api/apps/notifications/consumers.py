import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if not self.user:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def notification_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "message": event["message"],
                    "data": event.get("data", {}),
                }
            )
        )

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            token = self.scope["query_string"].decode().split("token=")[1]
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            return User.objects.get(id=user_id)
        except (IndexError, InvalidToken, User.DoesNotExist):
            return None


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if not self.user or self.user.role != "BOSS":
            await self.close()
            return

        self.room_group_name = "boss_dashboard"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def dashboard_update(self, event):
        await self.send(
            text_data=json.dumps({"type": "dashboard_update", "data": event["data"]})
        )

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            token = self.scope["query_string"].decode().split("token=")[1]
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            return User.objects.get(id=user_id)
        except (IndexError, InvalidToken, User.DoesNotExist):
            return None
