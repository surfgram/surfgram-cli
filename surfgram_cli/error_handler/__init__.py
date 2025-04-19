from rich.console import Console
from rich.panel import Panel
from functools import wraps
import traceback
import sys
from ..config import UIConfig

console = Console()


class ErrorHandler:
    """Centralized error handling for the CLI application"""

    @staticmethod
    def handle_error(e: Exception, full_trace: bool = False, context: str = ""):
        """Handle exceptions with proper error messages and optional context"""
        error_message = f"❌ {context + ': ' if context else ''}{str(e)}"
        console.print(Panel(error_message, title="Error", style=UIConfig.ERROR_STYLE))
        if full_trace:
            console.print(traceback.format_exc())

    @staticmethod
    def handle_keyboard_interrupt(operation: str):
        """Handle keyboard interruption with a consistent message"""
        console.print(f"\nOperation canceled", style=UIConfig.SUCCESS_STYLE)
        sys.exit(0)


def handle_exceptions(operation: str):
    """Decorator for handling common exceptions in CLI commands"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                ErrorHandler.handle_keyboard_interrupt(operation)
            except Exception as e:
                full_trace = kwargs.get("full_trace", False)
                ErrorHandler.handle_error(e, full_trace, operation)

        return wrapper

    return decorator
