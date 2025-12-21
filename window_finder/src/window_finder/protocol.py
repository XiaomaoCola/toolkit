# src/window_finder/protocol.py
from __future__ import annotations
from typing import Protocol, runtime_checkable, List, Optional
from .models import WindowInfo

@runtime_checkable
class WindowFinder(Protocol):
    """
    Interface for cross-platform window discovery.
    """

    def find_windows(self, keyword: str, *, case_sensitive: bool = False) -> List[WindowInfo]:
        """Return all visible windows whose title matches keyword."""

    def find_first(self, keyword: str, *, case_sensitive: bool = False) -> Optional[WindowInfo]:
        """Return the first matched window (or None)."""
