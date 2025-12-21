# src/window_finder/backends/win32.py
from __future__ import annotations
from typing import List, Optional, Tuple
import re

import ctypes
import win32gui
import win32process

from ..models import WindowInfo, RectLTRB


class Win32WindowFinder:
    """
    Win32 backend implementation.

    Notes:
    - native_id is hwnd (int)
    - rect_ltrb uses GetWindowRect (screen coordinates)
    """

    def __init__(self) -> None:
        # Avoid DPI scaling surprises in some environments
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    def find_windows(self, keyword: str, *, case_sensitive: bool = False) -> List[WindowInfo]:
        matches: List[WindowInfo] = []

        if not keyword:
            return matches

        # Prepare matcher
        if case_sensitive:
            def is_match(title: str) -> bool:
                return keyword in title
        else:
            low_kw = keyword.lower()
            def is_match(title: str) -> bool:
                return low_kw in title.lower()

        def enum_handler(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd) or ""
            if not title.strip():
                return

            if not is_match(title):
                return

            rect: Optional[RectLTRB] = None
            try:
                l, t, r, b = win32gui.GetWindowRect(hwnd)
                rect = (int(l), int(t), int(r), int(b))
            except Exception:
                rect = None

            pid: Optional[int] = None
            try:
                _, pid_ = win32process.GetWindowThreadProcessId(hwnd)
                pid = int(pid_)
            except Exception:
                pid = None

            matches.append(
                WindowInfo(
                    native_id=int(hwnd),
                    title=title,
                    rect_ltrb=rect,
                    pid=pid,
                    app_name=None,  # 进程名你也可以后面用 psutil 补上
                )
            )

        win32gui.EnumWindows(enum_handler, None)
        return matches

    def find_first(self, keyword: str, *, case_sensitive: bool = False) -> Optional[WindowInfo]:
        wins = self.find_windows(keyword, case_sensitive=case_sensitive)
        return wins[0] if wins else None
