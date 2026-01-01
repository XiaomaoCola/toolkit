from __future__ import annotations

from interaction_mouse import Button, Clicker, Point, Rect
from tests.conftest import FakeDriver


def test_click_calls_driver_in_order() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.click(Point(1, 2), button=Button.LEFT)

    names = [name for name, _, _ in d.calls]
    assert names == ["move_to", "down", "sleep", "up"]


def test_click_accepts_tuple_point_and_str_button() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.click((10, 20), button="left")

    # move_to args should reflect the tuple
    name0, args0, kwargs0 = d.calls[0]
    assert name0 == "move_to"
    assert args0 == (10, 20)
    assert "duration" in kwargs0

    # down should use Button enum
    name1, args1, _ = d.calls[1]
    assert name1 == "down"
    assert args1[0] == Button.LEFT


def test_clicks_repeat_count() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.clicks(Point(10, 20), count=3, interval=0.0, jitter_px=0, button=Button.LEFT)

    # Each click: move_to, down, sleep, up
    # 3 clicks => 12 calls total, plus intervals sleeps between clicks (2 sleeps)
    names = [name for name, _, _ in d.calls]
    assert names.count("down") == 3
    assert names.count("up") == 3
    assert names.count("move_to") == 3
    # sleep includes click_delay (3) + interval between clicks (2) => 5
    assert names.count("sleep") == 5


def test_clicks_accepts_list_point() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.clicks([10, 20], count=2, interval=0.0, jitter_px=0, button="right")

    names = [name for name, _, _ in d.calls]
    assert names.count("move_to") == 2
    assert names.count("down") == 2
    assert names.count("up") == 2

    # confirm right button was used
    downs = [args[0] for (name, args, _) in d.calls if name == "down"]
    assert downs == [Button.RIGHT, Button.RIGHT]


def test_rand_click_count() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.rand_click(Rect(0, 0, 10, 10), count=4, interval=0.0, avoid_edges_px=0, button=Button.LEFT)

    names = [name for name, _, _ in d.calls]
    assert names.count("down") == 4
    assert names.count("up") == 4
    assert names.count("move_to") == 4


def test_rand_click_accepts_tuple_rect() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.rand_click((0, 0, 10, 10), count=3, interval=0.0, avoid_edges_px=0, button="middle")

    names = [name for name, _, _ in d.calls]
    assert names.count("move_to") == 3
    downs = [args[0] for (name, args, _) in d.calls if name == "down"]
    assert downs == [Button.MIDDLE, Button.MIDDLE, Button.MIDDLE]


def test_drag_moves_steps() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.drag(Point(0, 0), Point(10, 0), duration=0.0, steps=5, button=Button.LEFT)

    names = [name for name, _, _ in d.calls]
    # move_to start + move_to steps
    assert names.count("move_to") == 1 + 5
    assert names.count("down") == 1
    assert names.count("up") == 1


def test_drag_accepts_tuple_points_and_str_button() -> None:
    d = FakeDriver()
    c = Clicker(driver=d, click_delay=0.0, move_duration=0.0)

    c.drag((0, 0), (10, 10), duration=0.0, steps=3, button="left")

    names = [name for name, _, _ in d.calls]
    assert names.count("move_to") == 1 + 3
    downs = [args[0] for (name, args, _) in d.calls if name == "down"]
    assert downs == [Button.LEFT]
