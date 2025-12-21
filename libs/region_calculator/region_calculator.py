from __future__ import annotations
from typing import Optional, Tuple

from .interfaces import IWindowLocator
from .region_mapper import NormalizedRect, norm_rect_to_pixels

Rect = Tuple[int, int, int, int]


class RegionCalculator:
    """
    Facade: uses a window locator to obtain client rect,
    then maps normalized rect -> pixel rect (relative to client).
    """

    def __init__(self, locator: IWindowLocator):
        self.locator = locator

    def get_region_coords(
        self,
        norm_left: float,
        norm_top: float,
        norm_right: float,
        norm_bottom: float,
    ) -> Optional[Rect]:
        info = self.locator.find()
        if info is None:
            return None

        n = NormalizedRect(norm_left, norm_top, norm_right, norm_bottom)
        n.validate()

        return norm_rect_to_pixels(info.rect, n)
