from __future__ import annotations

from dataclasses import dataclass

from ..models import Point, Rect
from ..timing import random_point_in_rect


@dataclass(frozen=True, slots=True)
class RandomRectTarget:
    """Pick a random point inside rect."""
    rect: Rect
    avoid_edges_px: int = 0

    def pick(self) -> Point:
        x, y = random_point_in_rect(
            self.rect.left, self.rect.top, self.rect.right, self.rect.bottom,
            avoid_edges_px=self.avoid_edges_px
        )
        return Point(x, y)
