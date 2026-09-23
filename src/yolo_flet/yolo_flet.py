import asyncio
import json
from typing import Any, Optional
from .types  import DetectionResult

import flet as ft


@ft.control("YoloService")  # must match `case "YoloService":` in Dart
class YoloService(ft.Service):
    src: Optional[str] = None
    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def init(self):
        self._channel: Optional[ft.DataChannel] = None
        self._channel_ready = asyncio.Event()
        self._pending: dict[bytes, asyncio.Future] = {}
        self._next_id = 0
        # Set BEFORE super().init(): that's where the service is sent to Flutter,
        # and Dart only fires data_channel_open if a handler was set by then.
        if self.on_data_channel_open is None:
            self.on_data_channel_open = lambda e: None
        super().init()

    def before_event(self, e):
        # Grab the channel here, so it works even with a user-supplied handler.
        if isinstance(e, ft.DataChannelOpenEvent):
            self._loop = asyncio.get_running_loop()
            self._channel = self.get_data_channel(e.channel_id)
            self._channel.on_bytes(self._on_bytes)
            self._channel_ready.set()
        return super().before_event(e)

    def _on_bytes(self, payload: bytes):
        # can be called off the event-loop thread in built apps
        self._loop.call_soon_threadsafe(self._resolve, payload[:4], payload[4:])

    def _resolve(self, request_id: bytes, body: bytes):
        fut = self._pending.pop(request_id, None)
        if fut is not None and not fut.done():
            fut.set_result(json.loads(body))

    async def detect_frame(self, image: bytes, timeout: float = 30) -> list[DetectionResult]:
        """Camera frames over the DataChannel. Await each call before sending the next."""
        await asyncio.wait_for(self._channel_ready.wait(), timeout)
        self._next_id = (self._next_id + 1) & 0xFFFFFFFF
        request_id = self._next_id.to_bytes(4, "little")
        fut = self._pending[request_id] = asyncio.get_running_loop().create_future()
        self._channel.send(request_id + image)
        try:
            reply = await asyncio.wait_for(fut, timeout)
        finally:
            self._pending.pop(request_id, None)
        if "error" in reply:
            raise RuntimeError(reply["error"])
        print(reply["boxes"])
        return reply["boxes"]

    async def detect_objects(self, image: bytes, timeout: float = 30) -> list[dict[str, Any]]:
        """One-off images over the regular protocol."""
        return await self._invoke_method(
            "detectObjects", {"image_bytes": image}, timeout=timeout
        )