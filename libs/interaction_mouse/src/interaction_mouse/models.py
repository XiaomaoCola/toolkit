from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Button(str, Enum):
    """
    目前只写了三个按钮：左键，右键，中键（滚轮按下）。

    首先在绝大部分自动化场景里，这三个按键基本上够用了，侧键之类的不大可能用到，
    其次pyautogui 本身也不稳定支持侧键。
    但是这是“可扩展点”，未来假如要用到的话，直接往这个枚举类里加就行了。
    """
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    def __post_init__(self) -> None:
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise TypeError("Point.x and Point.y must be int")


@dataclass(frozen=True, slots=True)
class Rect:
    left: int
    top: int
    right: int
    bottom: int

    def __post_init__(self) -> None:
        for name in ("left", "top", "right", "bottom"):
            v = getattr(self, name)
            if not isinstance(v, int):
                raise TypeError(f"Rect.{name} must be int")
        if self.right <= self.left or self.bottom <= self.top:
            raise ValueError("Rect must satisfy right>left and bottom>top")

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

@dataclass(frozen=True, slots=True)
class WindowNormalizedPoint:
    """
    A point defined by:
    - window keyword
    - normalized coordinates (0~1) inside client area
    """
    keyword: str
    x: float
    y: float
    button: Button = Button.LEFT

@dataclass(frozen=True, slots=True)
class WindowNormalizedRect:
    """
    A rectangle defined by:
    - window keyword
    - normalized rectangle (left, top, right, bottom) inside client area

    All coordinates are in normalized space [0.0, 1.0].
    """
    keyword: str
    left: float
    top: float
    right: float
    bottom: float
    button: Button = Button.LEFT