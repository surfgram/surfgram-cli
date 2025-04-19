from typing import Any
from rich.console import Console
from surfgram_cli.enums import LevelsEnum


class Debugger:
    """
    A flexible debugger class for logging messages with different levels, colors, and output formats.

    Attributes:
        debug_mode (bool):  Indicates if debug mode is enabled. If False, no logs are printed.
        level (LevelsEnum): The minimum log level to display.  Messages with a level lower
                           than this will not be printed.
        output_format (str): The format of the output message.
    """

    def __init__(
        self,
        debug_mode: bool = False,
        level: LevelsEnum = LevelsEnum.INFO,
        output_format: str = "{prefix} {message}",
    ) -> None:
        """
        Initializes the Debugger.

        Args:
            debug_mode:  Enables or disables debugging output.
            level: The minimum log level to display.
            output_format: The format of the output message.
        """
        self.debug_mode = debug_mode
        self.level = level
        self.output_format = output_format
        self.console = Console()

    def log(self, message: Any, level: LevelsEnum) -> None:
        """
        Logs a message to the console if debug mode is enabled and the message's
        log level is equal to or greater than the debugger's configured level.

        Args:
            message: The message to log.
            level: The log level of the message (e.g., INFO, ERROR).
        """
        if self.debug_mode:
            formatted_message = self.output_format.format(
                prefix=f"[{level.color}][{level.prefix}][/{level.color}]",
                message=message,
            )
            self.console.print(formatted_message)


debugger = Debugger()
