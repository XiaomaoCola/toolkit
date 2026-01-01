class InteractionMouseError(Exception):
    """Base error for interaction_mouse."""


class DriverError(InteractionMouseError):
    """Driver related error (missing dependency, OS limitation, etc.)."""


class ValidationError(InteractionMouseError):
    """Invalid user input / parameters."""


class ActionError(InteractionMouseError):
    """Action execution error."""
