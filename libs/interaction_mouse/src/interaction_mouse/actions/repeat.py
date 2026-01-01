from __future__ import annotations

from dataclasses import dataclass

from ..models import Button, Point
from ..protocol import IMouseDriver
from ..timing import Delay, sample_delay, jitter_point
from .click import ClickAction


@dataclass(slots=True)
class RepeatClickAction:
    driver: IMouseDriver
    click_delay: Delay = 0.01
    move_duration: Delay = 0.0

    def execute(
        self,
        point: Point,
        count: int = 1,
        interval: Delay = 0.0,
        jitter_px: int = 0,
        button: Button = Button.LEFT,
    ) -> None:
        click = ClickAction(self.driver, click_delay=self.click_delay, move_duration=self.move_duration)
        for i in range(max(0, int(count))):
            x, y = jitter_point(point.x, point.y, jitter_px=jitter_px)
            click.execute(Point(x, y), button=button)
            if i != count - 1:
                self.driver.sleep(sample_delay(interval))
