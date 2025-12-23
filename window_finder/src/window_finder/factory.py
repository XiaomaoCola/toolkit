# src/window_finder/factory.py
# 只有 factory 知道 backend 的存在，factory 是跟 backend 联动的。
# backend 不知道 factory。
# 用户 不知道 backend。
# 不是“所有高级包”都这样，但“只要跨平台，基本都会这样”。

from __future__ import annotations
import sys

from .protocol import WindowFinder
from .errors import NotSupportedError


def create_window_finder() -> WindowFinder:
    """
    Create a platform-appropriate WindowFinder implementation.
    """
    plat = sys.platform
    # 这是 Python 自带的“我是谁。Windows的时候plat == "win32"; macOS的时候，plat == "darwin"； Linux的时候，plat == "linux"。

    if plat.startswith("win"):
    # 用 startswith 是防御式写法，不是随便写的。Windows = "win32"， "win_amd64" 之类的都有可能。
        from .backends.win32 import Win32WindowFinder
        # Lazy Import（延迟导入）， “只有当我确认现在是 Windows，我才去加载 Windows 专用代码。”
        return Win32WindowFinder()

    # macOS / Linux 先不实现：你未来加 backends/macos.py, x11.py, wayland.py
    raise NotSupportedError(f"window_finder: platform not supported yet: {plat}")
