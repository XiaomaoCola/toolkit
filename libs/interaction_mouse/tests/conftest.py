from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from interaction_mouse.models import Button
from interaction_mouse.protocol import IMouseDriver


@dataclass
class FakeDriver(IMouseDriver):
    calls: List[Tuple[str, tuple, dict]] = field(default_factory=list)

    def move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        self.calls.append(("move_to", (x, y), {"duration": duration}))

    def down(self, button: Button = Button.LEFT) -> None:
        self.calls.append(("down", (button,), {}))

    def up(self, button: Button = Button.LEFT) -> None:
        self.calls.append(("up", (button,), {}))

    def sleep(self, seconds: float) -> None:
        self.calls.append(("sleep", (seconds,), {}))
