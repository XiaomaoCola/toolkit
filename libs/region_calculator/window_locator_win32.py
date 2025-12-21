import ctypes
import re
import win32gui

from .interfaces import IWindowLocator, WindowClientRect


class Win32KeywordWindowLocator(IWindowLocator):
    """
    Find a visible top-level window by title keyword (regex search),
    then return its *client rect* in screen coordinates.
    """

    def __init__(self, window_keyword: str = "BlueStacks"):
        self.window_keyword = window_keyword
        ctypes.windll.user32.SetProcessDPIAware()

    def find(self):
        matches = []

        def enum_handler(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = win32gui.GetWindowText(hwnd)
            if title and re.search(self.window_keyword, title, flags=re.I):
                matches.append((hwnd, title))

        win32gui.EnumWindows(enum_handler, None)

        if not matches:
            return None

        hwnd, title = matches[0]

        # client rect -> screen coords
        client_rect = win32gui.GetClientRect(hwnd)  # (0,0,w,h) in client coords
        left_top = win32gui.ClientToScreen(hwnd, (0, 0))
        left, top = left_top
        right = left + client_rect[2]
        bottom = top + client_rect[3]

        return WindowClientRect(hwnd=hwnd, title=title, rect=(left, top, right, bottom))
