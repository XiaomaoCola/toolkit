from __future__ import annotations

from dataclasses import dataclass

from ..models import Point


@dataclass(frozen=True, slots=True)
class FixedTarget:
    """Always return the same point."""
    point: Point

    def pick(self) -> Point:
        return self.point
