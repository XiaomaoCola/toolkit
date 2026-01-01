from __future__ import annotations

from dataclasses import dataclass
import random

from ..models import Point


@dataclass(frozen=True, slots=True)
class NearTarget:
    """Pick a point near a center within a radius (square radius)."""
    center: Point
    radius_px: int = 0

    def pick(self) -> Point:
        r = max(0, int(self.radius_px))
        if r == 0:
            return self.center
        dx = random.randint(-r, r)
        dy = random.randint(-r, r)
        return Point(self.center.x + dx, self.center.y + dy)
