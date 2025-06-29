import typer
from .ui_components import BannerComponent
from .ui_components import ConsoleComponent
from .error_handler import handle_exceptions

app = typer.Typer(help="Surfgram CLI - A modern Telegram bot framework")
banner = BannerComponent()
console = ConsoleComponent()


def print_banner():
    """Print a banner"""
    banner.print_banner()

def _version_callback(value: bool):
    if value:
        from . import __version__
        import surfgram
        
        typer.echo(
            f"Surfgram version: {surfgram.__version__}\n"
            f"Surfgram CLI version: {__version__}",
        )
        raise typer.Exit()


@app.callback()
def callback(
    no_graphics: bool = typer.Option(
        False, "--no-graphics", help="Disable ASCII banner display and all the graphics"
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """Global options for Surfgram CLI"""
    if not no_graphics:
        console.set_status(graphics=True)
        print_banner()


@app.command()
@handle_exceptions("Bot creation")
def new(
    bot_name: str,
    full_trace: bool = typer.Option(False, help="Show full error traceback"),
):
    """Create a new bot"""
    
    from surfgram_cli.manager import BotManager
    
    console.print_operation_header("🤖 Creating New Bot")
    token = console.prompt("🔑 Please enter your bot token", hide_input=True)

    if BotManager.create_bot(bot_name, token):
        console.print_success_message(
            f"✨ Bot '{bot_name}' created successfully!\n"
            "📁 Project structure initialized\n"
            "🚀 Ready to listen!"
        )
    else:
        console.print_cancel("Bot creation cancelled")


@app.command()
@handle_exceptions("Bot deletion")
def delete(
    bot_name: str,
    full_trace: bool = typer.Option(False, help="Show full error traceback"),
):
    """Delete the specified bot"""
    
    from surfgram_cli.manager import BotManager

    console.print_operation_header("🗑️ Delete Bot")

    if console.confirm(
        f"⚠️  Are you sure you want to delete the bot '{bot_name}'?", default=False
    ):
        BotManager.delete_bot(bot_name)
        console.print_success_message(f"✅ Bot '{bot_name}' has been deleted")
    else:
        console.print_cancel("Deletion cancelled.")


@app.command()
@handle_exceptions("Bot startup")
def run(
    bot: str = typer.Option(
        None,
        "--bot",
        "-b",
        help="Directory containing the bot. Defaults to current directory.",
        show_default=False,
    ),
    config: str = typer.Option(
        None,
        "--config",
        "-c",
        help="Config class in format 'module.ConfigClass'. Auto-detected if not specified.",
        show_default=False,
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode with verbose logging.",
        show_default=True,
    ),
    autoreload: bool = typer.Option(
        False,
        "--autoreload",
        help="Automatically reload bot on source changes.",
        show_default=True,
    ),
    full_trace: bool = typer.Option(
        False,
        "--full-trace",
        help="Show complete error tracebacks when enabled.",
        show_default=True,
    ),
):
    """Run the bot"""
    from surfgram_cli.manager import BotManager
    from pathlib import Path

    console.print_operation_header("🚀 Bot Startup")

    bot_dir = Path(bot).resolve() if bot else Path.cwd().resolve()
    if not config:
        config = BotManager.find_config(str(bot_dir))

    try:
        module_part, class_part = config.rsplit(".", 1)
        if not module_part or not class_part:
            raise ValueError("Invalid config format")
    except ValueError:
        console.print_error(
            f"Invalid config format: '{config}'\n"
            f"Expected format: 'module_name.ConfigClass'"
        )

    console.print_config_status(
        debug=debug, on_reload=autoreload, bot=str(bot_dir), config=config
    )

    BotManager.run_bot(
        bot=str(bot_dir), config=config, debug=debug, on_reload=autoreload
    )
