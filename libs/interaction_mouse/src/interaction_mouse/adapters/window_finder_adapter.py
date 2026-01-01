from __future__ import annotations
from ..models import Rect
from ..errors import DriverError

def get_client_rect(keyword: str) -> Rect:
    kw = keyword.strip()
    if not kw:
        raise DriverError("Window keyword is empty.")

    try:
        from window_finder import create_window_finder
    except ModuleNotFoundError as e:
        raise DriverError("window_finder not installed.") from e

    win = create_window_finder().find_first(kw)
    if not win:
        raise DriverError(f"Window not found: {kw}")

    l, t, r, b = win.client_rect_ltrb
    return Rect(l, t, r, b)
