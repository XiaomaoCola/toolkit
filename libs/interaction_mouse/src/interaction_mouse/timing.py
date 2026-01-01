from __future__ import annotations

import random
import time
from typing import Tuple, Union

Delay = Union[float, Tuple[float, float]]


def clamp_int(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def sample_delay(d: Delay) -> float:
    """Return a delay in seconds. Accepts float or (min,max)."""
    if isinstance(d, tuple):
        a, b = d
        if a > b:
            a, b = b, a
        return random.uniform(a, b)
    return float(d)


def sleep(seconds: Delay) -> None:
    time.sleep(sample_delay(seconds))


def jitter_point(x: int, y: int, jitter_px: int) -> tuple[int, int]:
    """Return (x,y) with +/- jitter_px random offset."""
    if jitter_px <= 0:
        return x, y
    dx = random.randint(-jitter_px, jitter_px)
    dy = random.randint(-jitter_px, jitter_px)
    return x + dx, y + dy


def random_point_in_rect(left: int, top: int, right: int, bottom: int, avoid_edges_px: int = 0) -> tuple[int, int]:
    """Pick a random point inside rect. Optionally avoid edges."""
    if avoid_edges_px < 0:
        avoid_edges_px = 0
    l = left + avoid_edges_px
    t = top + avoid_edges_px
    r = right - avoid_edges_px
    b = bottom - avoid_edges_px
    if r <= l or b <= t:
        # fallback: ignore avoid_edges
        l, t, r, b = left, top, right, bottom
    return random.randint(l, r - 1), random.randint(t, b - 1)
