import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs


class ChatConsumer(AsyncWebsocketConsumer):
    def _get_uid(self):
        # Require/accept ?uid=<value> in WS query string
        try:
            query_string = self.scope.get("query_string", b"").decode()
            if query_string:
                params = parse_qs(query_string)
                uid_from_query = params.get("uid", [None])[0]
                if uid_from_query:
                    return uid_from_query
        except Exception:
            pass

        return "unknown"

    def _group_name_from_uid(self, uid):
        safe_uid = str(uid).replace(":", "_").replace(".", "_").replace("/", "_")
        return f"chat_{safe_uid}"

    async def connect(self):
        uid = self._get_uid()
        self.group_name = self._group_name_from_uid(uid)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(json.dumps({
            "type": "message",
            "text": f"Connected to room for uid {uid}. You will receive updates in real time."
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", data)
        except json.JSONDecodeError:
            message = text_data

        await self.send(json.dumps({
            "type": "echo",
            "content": message
        }))

    async def broadcast_message(self, event):
        data = event.get("data")
        await self.send(json.dumps({
            "type": "broadcast",
            "content": data
        }))
