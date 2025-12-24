# src/window_finder/models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Union

RectLTRB = Tuple[int, int, int, int]  # left, top, right, bottom
# 这边是为了可读性，理由如下：
# 不定义RectLTRB = Tuple[int, int, int, int]的话，
# rect_ltrb: Optional[RectLTRB] = None 就会变成rect_ltrb: Optional[Tuple[int, int, int, int]] = None。

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
    # Union[int, str] 的意思是：“多选一”，即，要么是 int，要么是 str。
    # Optional[X]的意思是：Optional[X] == Union[X, None]。
    # 所以Optional[Union[int, str]]等价于：Union[int, str, None]。
    title: str
    rect_ltrb: Optional[RectLTRB] = None
    # = None 这是 默认值。这个意思是：如果创建 WindowInfo 时 不传 rect_ltrb，那它就是 None。
    pid: Optional[int] = None
    app_name: Optional[str] = None

    @property
    # @property = 把“由数据算出来的值”，伪装成“只读属性”，即“对数据的一种安全、统一、可维护的访问方式”。
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
