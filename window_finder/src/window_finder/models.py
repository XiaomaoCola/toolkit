# src/window_finder/models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Union

RectLTRB = Tuple[int, int, int, int]  # left, top, right, bottom

@dataclass(frozen=True)
class WindowInfo:
    """
    Cross-platform window info model.

    - native_id: platform-specific identifier (Win32: hwnd int)
    - title: window title
    - app_name / pid: optional (if available)
    - rect_ltrb: optional (some platforms may not provide)
    """
    native_id: Optional[Union[int, str]]
    title: str
    rect_ltrb: Optional[RectLTRB] = None
    pid: Optional[int] = None
    app_name: Optional[str] = None

    @property
    def left_top(self) -> Optional[Tuple[int, int]]:
        if not self.rect_ltrb:
            return None
        l, t, _, _ = self.rect_ltrb
        return (l, t)

    @property
    def width_height(self) -> Optional[Tuple[int, int]]:
        if not self.rect_ltrb:
            return None
        l, t, r, b = self.rect_ltrb
        return (max(0, r - l), max(0, b - t))

    @property
    def left_top_width_height(self) -> Optional[Tuple[int, int, int, int]]:
        if not self.rect_ltrb:
            return None
        l, t, r, b = self.rect_ltrb
        w = max(0, r - l)
        h = max(0, b - t)
        return (l, t, w, h)
