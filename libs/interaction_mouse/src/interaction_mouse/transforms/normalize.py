from __future__ import annotations

from ..models import Point, Rect, WindowNormalizedPoint, WindowNormalizedRect


def window_norm_point_to_screen_point(
    client: Rect,
    t: WindowNormalizedPoint,
) -> Point:
    """
    Convert a WindowNormalizedPoint to absolute screen Point.
    """
    x_norm = min(max(t.x, 0.0), 1.0)
    y_norm = min(max(t.y, 0.0), 1.0)
    # 这边是把 把 t.x_px , t.y_px 强制限制在 [0.0, 1.0] 这个区间里
    # 需要「先 max 再 min」。

    x_px = client.left + int(round(x_norm * client.width))
    y_px = client.top + int(round(y_norm * client.height))
    # round(x_px) = 四舍五入到“最近的整数”。
    # 例子：round(1.2)   输出是 1 ，round(1.6)   输出是 2 。
    return Point(x_px, y_px)


def window_norm_rect_to_screen_rect(client: Rect, target: WindowNormalizedRect) -> Rect:
    """
    Convert a WindowNormalizedRect (norm ltrb) to absolute screen Rect.
    """
    left_norm = min(max(target.left, 0.0), 1.0)
    top_norm = min(max(target.top, 0.0), 1.0)
    right_norm = min(max(target.right, 0.0), 1.0)
    bottom_norm = min(max(target.bottom, 0.0), 1.0)

    # 允许写反：自动修正
    if left_norm > right_norm:
        left_norm, right_norm = right_norm, left_norm
    if top_norm > bottom_norm:
        top_norm, bottom_norm = bottom_norm, top_norm

    left_px = client.left + int(round(left_norm * client.width))
    top_px = client.top + int(round(top_norm * client.height))
    right_px = client.left + int(round(right_norm * client.width))
    bottom_px = client.top + int(round(bottom_norm * client.height))
    # _px 意味着，这里已经从比例，变成了像素

    return Rect(left_px, top_px, right_px, bottom_px)
