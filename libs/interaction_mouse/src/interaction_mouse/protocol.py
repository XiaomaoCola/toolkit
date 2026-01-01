from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import Button


@runtime_checkable
class IMouseDriver(Protocol):
    """
    Lowest-level driver interface.

    我之前写过另一个Protocol，里面包含了 move_to, press, release 等5个方法。
    但是最终还是决定了down, up等，也就是目前的protocol更好。
    原因是：
    首先是，move_to, down, up, sleep，这是更“driver”的味道：最小原语（primitive operations）。
    其次是这四个更底、更小、更稳定，底层接口保持最小的话，未来加再多 Action 都不会被逼改 driver。
    最后是down/up 比 press/release 更贴近行业通用命名。
    """

    def move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        ...

    def down(self, button: Button = Button.LEFT) -> None:
        ...

    def up(self, button: Button = Button.LEFT) -> None:
        ...

    def sleep(self, seconds: float) -> None:
        ...
