from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from .yolo_flet import YoloFlet  # noqa

__all__ = [
    "DetectionResult"
]



@ft.value
class DetectionResult:
    """目标检测结果"""

    x1: float
    """左上角 x 坐标（原始像素）"""

    y1: float
    """左上角 y 坐标（原始像素）"""

    x2: float
    """右下角 x 坐标（原始像素）"""

    y2: float
    """右下角 y 坐标（原始像素）"""

    x1_norm: float
    """左上角 x 坐标（归一化）"""

    y1_norm: float
    """左上角 y 坐标（归一化）"""

    x2_norm: float
    """右下角 x 坐标（归一化）"""

    y2_norm: float
    """右下角 y 坐标（归一化）"""

    class_: str
    """检测目标类别（因 class 是关键字，使用 class_）"""

    class_name: str
    """类别名称"""

    confidence: float
    """置信度（检测准确率）"""