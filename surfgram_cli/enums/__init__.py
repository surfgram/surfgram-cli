from enum import Enum


class LevelsEnum(Enum):
    """
    Enum representing different log levels with associated color codes and prefixes.

    Attributes:
        INFO (tuple): Log level for informational messages.
        ERROR (tuple): Log level for error messages.
        API (tuple): Log level for API-related messages.

    Each enum member holds a tuple containing:
        - value (int): Numeric representation of the log level (used internally).
        - color (str): ANSI escape code for the text color.
        - prefix (str): String prefix for the log message.
    """

    INFO = (1, "green", "INFO")
    ERROR = (3, "red", "ERROR")
    API = (7, "magenta", "API")

    def __init__(self, value: int, color: str, prefix: str) -> None:
        """
        Initializes a LevelsEnum member.

        Args:
            value: Numeric value of the log level.
            color: ANSI escape code for the text color.
            prefix: String prefix for the log message.
        """
        self._value_ = value
        self.color = color
        self.prefix = prefix

    @property
    def reset_color(self) -> str:
        """
        Returns the ANSI escape code to reset the text color.

        Returns:
            The ANSI reset code.
        """
        return "\033[0m"
