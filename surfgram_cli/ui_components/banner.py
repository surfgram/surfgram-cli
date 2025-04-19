from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from ..config import UIConfig


class BannerComponent:
    """Component for rendering the application banner"""

    def __init__(self):
        self.console = Console()
        self._figlet = Figlet(font=UIConfig.BANNER_FONT)

    def _center_text(self, text: str) -> str:
        """Center text based on terminal width"""
        terminal_width = self.console.width
        padding = (terminal_width - len(text)) // 2
        return " " * padding + text

    def _render_figlet(self, text: str) -> str:
        """Render text using figlet and center each line"""
        figlet_text = self._figlet.renderText(text)
        return "\n".join(self._center_text(line) for line in figlet_text.split("\n"))

    def print_banner(self):
        """Print the main application banner"""
        try:
            # Render and center the figlet banner
            centered_figlet_text = self._render_figlet("Surfgram")
            text = Text(centered_figlet_text, style=UIConfig.BANNER_STYLE)
            self.console.print(Panel(text, border_style=UIConfig.BORDER_STYLE))

            # Print framework description
            centered_desc = self._center_text(UIConfig.FRAMEWORK_DESCRIPTION)
            self.console.print(f"{centered_desc}\n", style=UIConfig.FRAMEWORK_STYLE)

        except Exception as e:
            from ..error_handler import ErrorHandler

            ErrorHandler.handle_error(e, context="Banner printing")
