from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ..models import Button, Point, Rect
from ..protocol import IMouseDriver
from ..timing import Delay, sample_delay, random_point_in_rect
from .click import ClickAction


@dataclass(slots=True)
class RandomClickAction:
    driver: IMouseDriver
    click_delay: Delay = 0.01
    move_duration: Delay = 0.0

    def execute(
        self,
        rect: Rect,
        count: int = 1,
        interval: Delay = 0.0,
        avoid_edges_px: int = 0,
        button: Button = Button.LEFT,
    ) -> None:
        click = ClickAction(self.driver, click_delay=self.click_delay, move_duration=self.move_duration)
        n = max(0, int(count))
        for i in range(n):
            x, y = random_point_in_rect(rect.left, rect.top, rect.right, rect.bottom, avoid_edges_px=avoid_edges_px)
            click.execute(Point(x, y), button=button)
            if i != n - 1:
                self.driver.sleep(sample_delay(interval))
