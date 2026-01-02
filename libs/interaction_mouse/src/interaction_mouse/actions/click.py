from __future__ import annotations

from dataclasses import dataclass

from ..models import Button, Point
from ..protocol import IMouseDriver
from ..timing import Delay, sample_delay, jitter_point


@dataclass(slots=True)
class ClickAction:
    driver: IMouseDriver
    click_delay: Delay = 0.01
    move_duration: Delay = 0.0

    def execute(
        self,
        point: Point,
        button: Button = Button.LEFT,
        *,
        jitter_px: int = 0,
    ) -> None:
        x, y = jitter_point(point.x, point.y, jitter_px=int(jitter_px))
        self.driver.move_to(x, y, duration=sample_delay(self.move_duration))
        self.driver.down(button)
        self.driver.sleep(sample_delay(self.click_delay))
        self.driver.up(button)