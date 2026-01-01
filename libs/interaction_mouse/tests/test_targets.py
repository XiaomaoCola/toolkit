from __future__ import annotations

from interaction_mouse.models import Point, Rect
from interaction_mouse.targets import FixedTarget, NearTarget, RandomRectTarget


def test_fixed_target() -> None:
    p = Point(10, 20)
    t = FixedTarget(p)
    assert t.pick() == p
    assert t.pick() == p


def test_near_target_radius_zero() -> None:
    c = Point(10, 20)
    t = NearTarget(center=c, radius_px=0)
    assert t.pick() == c


def test_near_target_in_bounds() -> None:
    c = Point(100, 200)
    r = 5
    t = NearTarget(center=c, radius_px=r)
    for _ in range(200):
        p = t.pick()
        assert (c.x - r) <= p.x <= (c.x + r)
        assert (c.y - r) <= p.y <= (c.y + r)


def test_random_rect_target_in_bounds() -> None:
    rect = Rect(10, 20, 30, 40)
    t = RandomRectTarget(rect=rect, avoid_edges_px=0)
    for _ in range(200):
        p = t.pick()
        assert rect.left <= p.x < rect.right
        assert rect.top <= p.y < rect.bottom


def test_random_rect_target_avoid_edges() -> None:
    rect = Rect(0, 0, 10, 10)
    t = RandomRectTarget(rect=rect, avoid_edges_px=2)
    for _ in range(200):
        p = t.pick()
        assert 2 <= p.x < 8
        assert 2 <= p.y < 8
