# src/window_finder/__init__.py
from .models import WindowInfo
from .protocol import WindowFinder
from .factory import create_window_finder
from .errors import WindowFinderError, NotSupportedError, PermissionRequiredError

__all__ = [
    "WindowInfo",
    "WindowFinder",
    "create_window_finder",
    "WindowFinderError",
    "NotSupportedError",
    "PermissionRequiredError",
]
