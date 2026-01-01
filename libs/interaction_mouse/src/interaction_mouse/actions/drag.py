from __future__ import annotations

from dataclasses import dataclass

from ..models import Button, Point
from ..protocol import IMouseDriver
from ..timing import Delay, sample_delay


@dataclass(slots=True)
class DragAction:
    driver: IMouseDriver
    click_delay: Delay = 0.01
    move_duration: Delay = 0.0

    def execute(
        self,
        start: Point,
        end: Point,
        duration: float = 0.5,
        button: Button = Button.LEFT,
        steps: int = 20,
    ) -> None:
        # Move to start
        self.driver.move_to(start.x, start.y, duration=sample_delay(self.move_duration))
        self.driver.down(button)
        self.driver.sleep(sample_delay(self.click_delay))

        # Linear interpolation in steps (simple but solid)
        steps = max(1, int(steps))
        dur = max(0.0, float(duration))
        per = dur / steps if steps > 0 else 0.0

        for i in range(1, steps + 1):
            t = i / steps
            x = int(start.x + (end.x - start.x) * t)
            y = int(start.y + (end.y - start.y) * t)
            self.driver.move_to(x, y, duration=0.0)
            if per > 0:
                self.driver.sleep(per)

        self.driver.up(button)
