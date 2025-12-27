# src/window_finder/models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Union

RectLTRB = Tuple[int, int, int, int]  # left, top, right, bottom
# 这边是为了可读性，理由如下：
# 不定义RectLTRB = Tuple[int, int, int, int]的话，
# window_rect_ltrb: Optional[RectLTRB] = None 就会变成window_rect_ltrb: Optional[Tuple[int, int, int, int]] = None。

@dataclass(frozen=True)
class WindowInfo:
    """
    Cross-platform window info model.
    跨平台的窗口信息模型。

    - native_id: platform-specific identifier (Win32: hwnd int)，平台相关的窗口标识符（在 Windows 上是 hwnd 整数）
    - title: window title，窗口标题
    - app_name / pid: optional (if available)，可选信息（如果平台能够提供）
    - window_rect_ltrb: optional (some platforms may not provide)
    """
    native_id: Optional[Union[int, str]]
    # Union[int, str] 的意思是：“多选一”，即，要么是 int，要么是 str。
    # Optional[X]的意思是：Optional[X] == Union[X, None]。
    # 所以Optional[Union[int, str]]等价于：Union[int, str, None]。
    title: str
    window_rect_ltrb: Optional[RectLTRB] = None
    # = None 这是 默认值。这个意思是：如果创建 WindowInfo 时 不传 rect_ltrb，那它就是 None。
    client_rect_ltrb: Optional[RectLTRB] = None
    pid: Optional[int] = None
    app_name: Optional[str] = None

    # ---------- window rect ----------
    @property
    # @property = 把“由数据算出来的值”，伪装成“只读属性”，即“对数据的一种安全、统一、可维护的访问方式”。
    def window_left_top(self) -> Optional[Tuple[int, int]]:
        if not self.window_rect_ltrb:
            return None
        l, t, _, _ = self.window_rect_ltrb
        return (l, t)

    @property
    def window_width_height(self) -> Optional[Tuple[int, int]]:
        if not self.window_rect_ltrb:
            return None
        l, t, r, b = self.window_rect_ltrb
        return (max(0, r - l), max(0, b - t))

    @property
    def window_left_top_width_height(self) -> Optional[Tuple[int, int, int, int]]:
        if not self.window_rect_ltrb:
            return None
        l, t, r, b = self.window_rect_ltrb
        return (l, t, max(0, r - l), max(0, b - t))

    # ---------- client rect ----------
    @property
    def client_left_top(self):
        if not self.client_rect_ltrb:
            return None
        l, t, _, _ = self.client_rect_ltrb
        return (l, t)

    @property
    def client_width_height(self):
        if not self.client_rect_ltrb:
            return None
        l, t, r, b = self.client_rect_ltrb
        return (max(0, r - l), max(0, b - t))

    @property
    def client_left_top_width_height(self):
        if not self.client_rect_ltrb:
            return None
        l, t, r, b = self.client_rect_ltrb
        return (l, t, max(0, r - l), max(0, b - t))
