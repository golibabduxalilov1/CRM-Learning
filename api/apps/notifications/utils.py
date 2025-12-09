from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification(user_id, message, data=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {"type": "notification_message", "message": message, "data": data or {}},
    )


def send_dashboard_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "boss_dashboard", {"type": "dashboard_update", "data": data}
    )
