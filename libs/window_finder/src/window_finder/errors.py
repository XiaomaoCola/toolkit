# src/window_finder/errors.py
class WindowFinderError(Exception):
    pass

class NotSupportedError(WindowFinderError):
    """Platform not supported or feature not supported (e.g., Wayland restrictions)."""

class PermissionRequiredError(WindowFinderError):
    """Permissions required (common on macOS Accessibility)."""
