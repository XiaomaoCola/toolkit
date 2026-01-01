"""
win32：系统底层、强、快、适合游戏/模拟器
pyautogui：通用、跨平台、像模拟人操作、会移动真实鼠标

Windows 游戏/模拟器优先 win32，其它平台默认 pyautogui。

这个__init__.py文件 有一个重要功能，它是一个 driver 选择器（driver factory / selector）。
"""

from __future__ import annotations

import os
import platform
from typing import Optional

from ..errors import DriverError
from ..protocol import IMouseDriver


def get_default_driver(preferred: Optional[str] = None) -> IMouseDriver:
    """
    Select a driver.

    preferred:
      - "win32": use Win32 driver (Windows only)
      - "pyautogui": use pyautogui driver
      - None/"auto": choose sensible default by platform
    """
    name = (preferred or os.getenv("INTERACTION_MOUSE_DRIVER") or "auto").lower()
    # os.getenv("INTERACTION_MOUSE_DRIVER")是在读系统环境变量。
    # 例子： 在Windows（PowerShell）里输入$env:INTERACTION_MOUSE_DRIVER="pyautogui"，
    # Linux / macOS里输入export INTERACTION_MOUSE_DRIVER=pyautogui。 这样os.getenv("INTERACTION_MOUSE_DRIVER")就会返回"pyautogui"。
    # 环境变量的意义：不改代码，不动源码，只通过“运行环境”控制行为。这在工程里非常常见（部署 / CI / 自动化时尤其重要）。
    sysname = platform.system().lower()

    if name in ("auto", "", "default"):
        if sysname == "windows":
            name = "win32"
        else:
            name = "pyautogui"

    if name == "win32":
        if sysname != "windows":
            raise DriverError("win32 driver is only available on Windows.")
        from .win32 import Win32Driver

        return Win32Driver()

    if name == "pyautogui":
        from .pyautogui import PyAutoGuiDriver

        return PyAutoGuiDriver()

    raise DriverError(f"Unknown driver '{name}'. Available: auto, win32, pyautogui. OS={platform.system()}")
