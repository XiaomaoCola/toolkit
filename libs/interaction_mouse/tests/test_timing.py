from __future__ import annotations

import math

import pytest

from interaction_mouse.timing import (
    clamp_int,
    jitter_point,
    random_point_in_rect,
    sample_delay,
)


def test_clamp_int_basic() -> None:
    assert clamp_int(5, 0, 10) == 5
    assert clamp_int(-1, 0, 10) == 0
    assert clamp_int(99, 0, 10) == 10


def test_sample_delay_float() -> None:
    assert sample_delay(0.123) == pytest.approx(0.123)


def test_sample_delay_tuple_in_range() -> None:
    # run multiple times to reduce flake possibility
    for _ in range(50):
        d = sample_delay((0.01, 0.02))
        assert 0.01 <= d <= 0.02


def test_sample_delay_tuple_swapped_ok() -> None:
    for _ in range(20):
        d = sample_delay((0.02, 0.01))
        assert 0.01 <= d <= 0.02


def test_jitter_point_zero() -> None:
    assert jitter_point(10, 20, 0) == (10, 20)
    assert jitter_point(10, 20, -5) == (10, 20)


def test_jitter_point_in_bounds() -> None:
    x, y = 100, 200
    j = 3
    for _ in range(100):
        xx, yy = jitter_point(x, y, j)
        assert (x - j) <= xx <= (x + j)
        assert (y - j) <= yy <= (y + j)


def test_random_point_in_rect_basic() -> None:
    left, top, right, bottom = 10, 20, 30, 50
    for _ in range(200):
        x, y = random_point_in_rect(left, top, right, bottom, avoid_edges_px=0)
        assert left <= x < right
        assert top <= y < bottom


def test_random_point_in_rect_avoid_edges() -> None:
    left, top, right, bottom = 0, 0, 10, 10
    avoid = 2
    # valid inner area is [2,7] for randint inclusive endpoints; but we use < right so max 7
    for _ in range(200):
        x, y = random_point_in_rect(left, top, right, bottom, avoid_edges_px=avoid)
        assert 2 <= x < 8
        assert 2 <= y < 8


def test_random_point_in_rect_avoid_edges_too_large_fallback() -> None:
    # avoid_edges makes inner invalid; function should fallback to full rect
    left, top, right, bottom = 0, 0, 5, 5
    avoid = 100
    for _ in range(200):
        x, y = random_point_in_rect(left, top, right, bottom, avoid_edges_px=avoid)
        assert left <= x < right
        assert top <= y < bottom
