from enum import Enum
from typing import Any, Optional
import flet as ft
from .types import DetectionResult


@ft.control("YoloFlet")
class YoloFlet(ft.Service):
    """
    YoloFlet Control description.
    """

    src: str

    async def detect(self, image: bytes) -> list[DetectionResult]:

        return await self._invoke_method(method_name= "detectObjects",arguments={"image_bytes":image})