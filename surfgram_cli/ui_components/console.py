from ..config import UIConfig
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer

from ..config import UIConfig


class ConsoleComponent:
    """Component for consistent console output and status messages"""

    def __init__(self):
        self._graphics_enabled: bool = False  # Приватное поле для хранения состояния
        self.console = None  # Инициализация отложена до первого вызова
        self._init_console()  # Сразу инициализируем консоль

    def _init_console(self):
        """Initialize console based on graphics_enabled"""
        if self._graphics_enabled:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text

            self.console = Console()
        else:
            self.console = None  # В текстовом режиме rich не используется

    def set_status(self, graphics: bool = True) -> None:
        """Enable/disable rich graphics and immediately apply changes"""
        if self._graphics_enabled != graphics:  # Если состояние изменилось
            self._graphics_enabled = graphics
            self._init_console()  # Переинициализируем консоль

    @property
    def graphics_enabled(self) -> bool:
        """Check if rich graphics are enabled"""
        return self._graphics_enabled

    def print_operation_header(self, message: str) -> None:
        """Print a header for an operation"""
        if self._graphics_enabled:
            self.console.print(Panel.fit(message, style=UIConfig.ACCENT_STYLE))

    def print_success_message(self, message: str, title: str = "Success") -> None:
        """Print a success message in a panel"""
        if self._graphics_enabled:
            self.console.print(
                Panel(message, title=title, style=UIConfig.SUCCESS_STYLE)
            )

    def print_cancel(self, message: str) -> None:
        """Print a cancel message"""
        if self._graphics_enabled:
            self.console.print(f"[yellow]{message}[/]")

    def print_error(self, message: str) -> None:
        """Print an error message"""
        if self._graphics_enabled:
            self.console.print(f"[red]{message}[/]")

    def confirm(self, message: str, default: bool = False) -> bool:
        """Show a confirmation prompt (uses typer, unaffected by graphics mode)"""
        return typer.confirm(message, default=default)

    def prompt(self, message: str, hide_input: bool = False) -> str:
        """Show an input prompt (uses typer, unaffected by graphics mode)"""
        return typer.prompt(message, hide_input=hide_input)

    def print_config_status(
        self, debug: bool, on_reload: bool, bot: str, config: str
    ) -> None:
        """Print configuration status"""
        status_text = "🔧 Debug mode enabled\n" if debug else ""
        status_text += "🔄 Auto-reload enabled\n" if on_reload else ""
        status_text += f"📂 Bot: {bot}\n"
        status_text += f"⚙️ Config: {config}"

        if self._graphics_enabled:
            self.console.print(
                Panel(status_text, title="Configuration", style=UIConfig.ACCENT_STYLE)
            )
