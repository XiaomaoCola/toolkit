# src/window_finder/factory.py
from __future__ import annotations
import sys

from .protocol import WindowFinder
from .errors import NotSupportedError


def create_window_finder() -> WindowFinder:
    """
    Create a platform-appropriate WindowFinder implementation.
    """
    plat = sys.platform

    if plat.startswith("win"):
        from .backends.win32 import Win32WindowFinder
        return Win32WindowFinder()

    # macOS / Linux 先不实现：你未来加 backends/macos.py, x11.py, wayland.py
    raise NotSupportedError(f"window_finder: platform not supported yet: {plat}")
