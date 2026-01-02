from __future__ import annotations

"""
clicker的职能是：把“点击意图”变成“driver 调用”

Main facade interface for mouse interactions.
This module provides the Clicker class, which serves as the primary
entry point for mouse interaction functionality.
"""

from typing import Optional, Sequence, Tuple, Union, overload

from .models import Button, Point, Rect, WindowNormalizedPoint, WindowNormalizedRect
from .protocol import IMouseDriver
from .drivers import get_default_driver
from .timing import Delay
from .actions import ClickAction, RepeatClickAction, RandomClickAction, DragAction
from .adapters.window_finder_adapter import get_client_rect
from .transforms.normalize import window_norm_point_to_screen_point, window_norm_rect_to_screen_rect


PointLike = Union[Point, Tuple[int, int], Sequence[int]]
RectLike = Union[Rect, Tuple[int, int, int, int], Sequence[int]]
ButtonLike = Union[Button, str]
# 这是为了让用户调用更爽，不用强制他们必须构造 Point/Rect 才能用。


def _as_point(p: PointLike) -> Point:
    """
    把各种“PointLike”输入统一转换成标准类型的 Point。
    """
    if isinstance(p, Point):
    # isinstance(p, Point) 的意思是 ： 判断变量 p 是不是 Point 这个类型（或它的子类）的实例，
    # 如果是 → True， 不是 → False。
        return p
    if isinstance(p, tuple) and len(p) == 2:
        x, y = p
        return Point(int(x), int(y))
    # allow list/sequence
    if isinstance(p, Sequence) and len(p) == 2:
        x, y = p[0], p[1]
        return Point(int(x), int(y))
    raise TypeError(f"Invalid point: {p!r}. Expected Point or (x, y).")


def _as_rect(r: RectLike) -> Rect:
    if isinstance(r, Rect):
        return r
    if isinstance(r, tuple) and len(r) == 4:
        l, t, rr, b = r
        return Rect(int(l), int(t), int(rr), int(b))
    if isinstance(r, Sequence) and len(r) == 4:
        l, t, rr, b = r[0], r[1], r[2], r[3]
        return Rect(int(l), int(t), int(rr), int(b))
    raise TypeError(f"Invalid rect: {r!r}. Expected Rect or (left, top, right, bottom).")


def _as_button(b: ButtonLike) -> Button:
    if isinstance(b, Button):
        return b
    if isinstance(b, str):
        s = b.strip().lower()
        if s in ("left", "l"):
            return Button.LEFT
        if s in ("right", "r"):
            return Button.RIGHT
        if s in ("middle", "mid", "m"):
            return Button.MIDDLE
    raise TypeError(f"Invalid button: {b!r}. Expected Button or 'left'/'right'/'middle'.")


class Clicker:
    """
    Main interface for mouse interactions.

    Supports flexible input:
    - Point or (x, y)
    - Rect or (left, top, right, bottom)
    - Button enum or string
    """

    def __init__(
        self,
        driver: Optional[IMouseDriver] = None,
        click_delay: Delay = 0.01,
        move_duration: Delay = 0.0,
    ) -> None:
        self.driver = driver if driver is not None else get_default_driver()
        self.click_delay = click_delay
        self.move_duration = move_duration

    def _ctx(self) -> dict:
        return {
            "driver": self.driver,
            "click_delay": self.click_delay,
            "move_duration": self.move_duration,
        }

    def click(self, point: PointLike, button: ButtonLike = Button.LEFT, *, jitter_px: int = 0) -> None:
        p = _as_point(point)
        b = _as_button(button)
        ClickAction(**self._ctx()).execute(point=p, button=b, jitter_px=int(jitter_px))

    def clicks(
        self,
        point: PointLike,
        count: int = 1,
        interval: Delay = 0.0,
        jitter_px: int = 0,
        button: ButtonLike = Button.LEFT,
    ) -> None:
        p = _as_point(point)
        b = _as_button(button)
        RepeatClickAction(**self._ctx()).execute(
            point=p,
            count=int(count),
            interval=interval,
            jitter_px=int(jitter_px),
            button=b,
        )

    def rand_click(
        self,
        rect: RectLike,
        count: int = 1,
        interval: Delay = 0.0,
        avoid_edges_px: int = 0,
        button: ButtonLike = Button.LEFT,
    ) -> None:
        rr = _as_rect(rect)
        b = _as_button(button)
        RandomClickAction(**self._ctx()).execute(
            rect=rr,
            count=int(count),
            interval=interval,
            avoid_edges_px=int(avoid_edges_px),
            button=b,
        )

    def drag(
        self,
        start: PointLike,
        end: PointLike,
        duration: float = 0.5,
        steps: int = 20,
        button: ButtonLike = Button.LEFT,
    ) -> None:
        s = _as_point(start)
        e = _as_point(end)
        b = _as_button(button)
        DragAction(**self._ctx()).execute(
            start=s,
            end=e,
            duration=float(duration),
            steps=int(steps),
            button=b,
        )

    def click_window_norm_point(self, target: WindowNormalizedPoint, *, jitter_px: int = 0) -> None:
        """
        Click a normalized point inside a window client area.

        之所以叫这个名字click_window_norm_point，
        第一是为了跟WindowNormalizedPoint对应，
        其次是未来要加新的函数click_window_norm_rect和新的变量WindowNormalizedRect，从而便于区分。
        """
        client = get_client_rect(target.keyword)
        pt = window_norm_point_to_screen_point(client, target)

        ClickAction(**self._ctx()).execute(
            point=pt,
            button=target.button,
            jitter_px=jitter_px,
        )

    def click_window_norm_rect_rand(
        self,
        target: WindowNormalizedRect,
        *,
        count: int = 1,
        interval: Delay = 0.0,
        avoid_edges_px: int = 0,
    ) -> None:
        """
        Random click inside a normalized rect inside a window client area.
        """
        client = get_client_rect(target.keyword)
        screen_rect = window_norm_rect_to_screen_rect(client, target)

        RandomClickAction(**self._ctx()).execute(
            rect=screen_rect,
            count=max(0, int(count)),
            interval=interval,
            avoid_edges_px=int(avoid_edges_px),
            button=target.button,
        )