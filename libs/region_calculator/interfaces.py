from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol, Tuple

Rect = Tuple[int, int, int, int]  # (left, top, right, bottom)
# 上面的那个井号键#注释很重要，它注释了这4个int的明确语义。
# 放在最前面的原因：这是一个约定俗成的工程习惯。

@dataclass(frozen=True)
class WindowClientRect:
    hwnd: int
    title: str
    rect: Rect  # client rect mapped to screen coords

class IWindowLocator(Protocol):
    def find(self) -> Optional[WindowClientRect]:
        ...
# Protocol + ... 这个语法的意思是：这是一个接口，不是实现。