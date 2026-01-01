from __future__ import annotations

import time
import ctypes
from ctypes import wintypes

# compat: ULONG_PTR may be missing on some Python builds
if not hasattr(wintypes, "ULONG_PTR"):
    wintypes.ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

from ..errors import DriverError
from ..models import Button


# ============================================================
# Win32 bindings
# ============================================================

user32 = ctypes.WinDLL("user32", use_last_error=True)

# --- SetCursorPos -------------------------------------------------

user32.SetCursorPos.argtypes = (wintypes.INT, wintypes.INT)
user32.SetCursorPos.restype = wintypes.BOOL

# --- GetCursorPos -------------------------------------------------

user32.GetCursorPos.argtypes = (ctypes.POINTER(wintypes.POINT),)
user32.GetCursorPos.restype = wintypes.BOOL

# --- SendInput ----------------------------------------------------

INPUT_MOUSE = 0

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_ABSOLUTE = 0x8000

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class INPUT(ctypes.Structure):
    class _INPUTUNION(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _anonymous_ = ("union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUTUNION),
    ]


user32.SendInput.argtypes = (
    wintypes.UINT,
    ctypes.POINTER(INPUT),
    ctypes.c_int,
)
user32.SendInput.restype = wintypes.UINT


# ============================================================
# Helpers
# ============================================================

def _raise_last_error(msg: str) -> None:
    err = ctypes.get_last_error()
    raise DriverError(f"{msg}. GetLastError={err}")


def _mouse_flags_for_button(button: Button, is_down: bool) -> int:
    if button == Button.LEFT:
        return MOUSEEVENTF_LEFTDOWN if is_down else MOUSEEVENTF_LEFTUP
    if button == Button.RIGHT:
        return MOUSEEVENTF_RIGHTDOWN if is_down else MOUSEEVENTF_RIGHTUP
    if button == Button.MIDDLE:
        return MOUSEEVENTF_MIDDLEDOWN if is_down else MOUSEEVENTF_MIDDLEUP
    raise DriverError(f"Unsupported button: {button}")


# ============================================================
# Driver implementation
# ============================================================

class Win32Driver:
    """
    Windows mouse driver using Win32 APIs.

    Implementation:
    - Cursor movement: SetCursorPos (foreground, real cursor)
    - Button events: SendInput

    Notes:
    - This driver WILL move the real mouse cursor.
    - No external dependencies.
    """

    def __init__(self) -> None:
        # Very basic sanity check
        if ctypes.sizeof(ctypes.c_void_p) not in (4, 8):
            raise DriverError("Invalid pointer size; Win32 driver init failed.")

    # --------------------------------------------------------

    def move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        """
        Move cursor to (x, y).

        If duration > 0, perform simple linear interpolation.
        """
        x = int(x)
        y = int(y)

        if duration <= 0:
            ok = user32.SetCursorPos(x, y)
            if not ok:
                _raise_last_error("SetCursorPos failed")
            return

        # Get current cursor position
        pt = wintypes.POINT()
        if not user32.GetCursorPos(ctypes.byref(pt)):
            _raise_last_error("GetCursorPos failed")

        x0, y0 = pt.x, pt.y

        # Interpolate with ~10ms step
        steps = max(1, int(duration / 0.01))
        sleep_per_step = duration / steps

        for i in range(1, steps + 1):
            t = i / steps
            xi = int(x0 + (x - x0) * t)
            yi = int(y0 + (y - y0) * t)

            ok = user32.SetCursorPos(xi, yi)
            if not ok:
                _raise_last_error("SetCursorPos failed during interpolation")

            time.sleep(sleep_per_step)

    # --------------------------------------------------------

    def down(self, button: Button = Button.LEFT) -> None:
        """
        Press mouse button down.
        """
        flags = _mouse_flags_for_button(button, is_down=True)

        inp = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(
                dx=0,
                dy=0,
                mouseData=0,
                dwFlags=flags,
                time=0,
                dwExtraInfo=0,
            ),
        )

        sent = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
        if sent != 1:
            _raise_last_error("SendInput (button down) failed")

    # --------------------------------------------------------

    def up(self, button: Button = Button.LEFT) -> None:
        """
        Release mouse button.
        """
        flags = _mouse_flags_for_button(button, is_down=False)

        inp = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(
                dx=0,
                dy=0,
                mouseData=0,
                dwFlags=flags,
                time=0,
                dwExtraInfo=0,
            ),
        )

        sent = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
        if sent != 1:
            _raise_last_error("SendInput (button up) failed")

    # --------------------------------------------------------

    def sleep(self, seconds: float) -> None:
        """
        Sleep helper (delegated to time.sleep).
        """
        time.sleep(max(0.0, float(seconds)))
