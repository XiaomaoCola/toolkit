from __future__ import annotations

from ..models import Point, Rect, WindowNormalizedPoint


def window_norm_to_screen_point(
    client: Rect,
    t: WindowNormalizedPoint,
) -> Point:
    """
    Convert a WindowNormalizedPoint to absolute screen Point.
    """
    x_norm = min(max(t.x, 0.0), 1.0)
    y_norm = min(max(t.y, 0.0), 1.0)
    # 这边是把 把 t.x , t.y 强制限制在 [0.0, 1.0] 这个区间里
    # 需要「先 max 再 min」。

    x = client.left + int(round(x_norm * client.width))
    y = client.top + int(round(y_norm * client.height))
    # round(x) = 四舍五入到“最近的整数”。
    # 例子：round(1.2)   输出是 1 ，round(1.6)   输出是 2 。
    return Point(x, y)
