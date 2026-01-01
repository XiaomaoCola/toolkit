from __future__ import annotations

import time

from interaction_mouse.src.interaction_mouse.errors import DriverError
from interaction_mouse.src.interaction_mouse.models import Button


class PyAutoGuiDriver:
    """
    Foreground driver using pyautogui.
    - Moves the real mouse cursor.
    - Works cross-platform.
    """

    def __init__(self) -> None:
        try:
            import pyautogui  # type: ignore
        except Exception as e:  # pragma: no cover
            raise DriverError(
                "pyautogui is not installed. Install with: pip install interaction-mouse[pyautogui]"
            ) from e
        self._pg = pyautogui

        # optional safety: disable failsafe if you don't want mouse corner abort
        # self._pg.FAILSAFE = False

    def move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        self._pg.moveTo(x, y, duration=duration)

    def down(self, button: Button = Button.LEFT) -> None:
        self._pg.mouseDown(button=button.value)
        # .value 是 枚举里的“真实值”。

    def up(self, button: Button = Button.LEFT) -> None:
        self._pg.mouseUp(button=button.value)

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
