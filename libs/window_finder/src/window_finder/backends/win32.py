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
        # 这里面有个星号 * 的意思是：从这里往后，参数只能用“关键字方式”传。
        # 例子：def f(a, b):   print(a, b)。 前面这个代码 f(1, 2) 和 f(1, b=2) 都可以得到 (1,2)这个结果。
        # 但是有 * 的情况， def f(a, *, b):  print(a, b)。 就只能f(1, b=2)才行， b这个关键字得写出来。
        matches: List[WindowInfo] = []
        # 其他格式的例子：x: int = 10，y: str = "hello"。
        # 前面的部分matches: List[WindowInfo]，叫做类型注释。当然后面必须 加上 = []。
        # 写成matches = []也行，但是，IDE 不知道里面该放啥，容易误用。

        if not keyword:
            return matches

        # Prepare matcher
        if case_sensitive:
            def is_match(title: str) -> bool:
                return keyword in title
            # in 这个语法是用来“子串判断”。
            # 例子： "abc" in "xxabcxx"   这会返回True  ，  "abc" in "ab"   这会返回False 。
        else:
            low_kw = keyword.lower()
            # .lower() 的意思是：把字符串全部变成小写。
            def is_match(title: str) -> bool:
                return low_kw in title.lower()

        def enum_handler(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return
            # IsWindowVisible(hwnd)：窗口是否可见（visible）。
            # 不可见的直接跳过（return 结束这次回调）。

            title = win32gui.GetWindowText(hwnd) or ""
            # GetWindowText(hwnd)：获取窗口标题栏文字，比如 “Google Chrome”。
            # 有些窗口可能返回 "" 或 None，所以用 or "" 保底，确保 title 一定是字符串，避免后面 .strip() 报错。
            if not title.strip():
                return
            # title.strip() 会去掉左右空格，如果去掉空格后还是空字符串，说明标题就是空的。

            if not is_match(title):
                return

            # ---------------- window rect (外框) ----------------
            window_rect: Optional[RectLTRB] = None
            try:
                l, t, r, b = win32gui.GetWindowRect(hwnd)
                window_rect = (int(l), int(t), int(r), int(b))
            except Exception:
                window_rect = None
            # GetWindowRect(hwnd) 返回4 个数：l, t, r, b。

            # ---------------- client rect (客户区) ----------------
            client_rect: Optional[RectLTRB] = None
            try:
                cl, ct, cr, cb = win32gui.GetClientRect(hwnd)  # (0,0,cw,ch) in client coords
                # GetClientRect 得到的是“客户区自身坐标系”，左上角永远是 (0,0)

                client_left_top = win32gui.ClientToScreen(hwnd, (0, 0))
                screen_cx, screen_cy = int(client_left_top[0]), int(client_left_top[1])
                # ClientToScreen(hwnd, (0, 0)) 相当于问 Windows：“这个窗口的客户区左上角 (0,0)，在屏幕上的位置是多少？”

                cw = int(cr - cl)
                ch = int(cb - ct)
                client_rect = (screen_cx, screen_cy, screen_cx + max(0, cw), screen_cy + max(0, ch))
                # 右下角 = 左上角 + (cw, ch)
            except Exception:
                client_rect = None

            # ---------------- pid ----------------
            pid: Optional[int] = None
            try:
                _, pid_ = win32process.GetWindowThreadProcessId(hwnd)
                pid = int(pid_)
            except Exception:
                pid = None
            # GetWindowThreadProcessId(hwnd) 返回：(thread_id, process_id)。

            matches.append(
                WindowInfo(
                    native_id=int(hwnd),
                    title=title,
                    window_rect_ltrb=window_rect,
                    client_rect_ltrb=client_rect,
                    pid=pid,
                    app_name=None,  # 进程名你也可以后面用 psutil 补上
                )
            )

        win32gui.EnumWindows(enum_handler, None)
        # “让 Windows 把当前系统里所有窗口，一个一个拿出来，
        # 对每一个窗口都调用一次 enum_handler，并把窗口的句柄 hwnd 传给它。”
        # 例子（原理一样）：
        # def walk(callback, data):
        #     for x in [1, 2, 3]:
        #         callback(x, data)
        # def handler(x, _):
        #     print(x)
        # walk(handler, None)
        return matches

    def find_first(self, keyword: str, *, case_sensitive: bool = False) -> Optional[WindowInfo]:
        wins = self.find_windows(keyword, case_sensitive=case_sensitive)
        return wins[0] if wins else None
