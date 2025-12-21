from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Rect = Tuple[int, int, int, int]


@dataclass(frozen=True)
# @dataclass 可以让我直接： n = NormalizedRect(0, 0.75, 0.15, 1)
# frozen=True 表示：这个对象一旦创建，就不可修改。   例子： n.left = 0.2  ❌ 就会直接报错
class NormalizedRect:
    left: float
    top: float
    right: float
    bottom: float

    def validate(self) -> None:
    # 不变式（Invariant）检查。
        for name, v in [("left", self.left), ("top", self.top), ("right", self.right), ("bottom", self.bottom)]:
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"{name} must be in [0, 1], got {v}")
        # 这边是保证每个值在 [0, 1]中。
        if self.right < self.left or self.bottom < self.top:
            raise ValueError("right/bottom must be >= left/top")
        # 这边是确保right ≥ left， bottom ≥ top。


def norm_rect_to_pixels(client_rect_on_screen: Rect, n: NormalizedRect) -> Rect:
    """
    Convert normalized rect (0..1) into pixel rect relative to the client area.
    NOTE: This returns *relative-to-client* pixel coords (same behavior as your original code).
    """
    left, top, right, bottom = client_rect_on_screen
    w = right - left
    h = bottom - top

    region_left = int(n.left * w)
    region_top = int(n.top * h)
    region_right = int(n.right * w)
    region_bottom = int(n.bottom * h)

    return (region_left, region_top, region_right, region_bottom)
