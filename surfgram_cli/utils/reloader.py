import watchdog.events
import watchdog.observers
import time
import os
import sys
import importlib.util
from . import debugger
from surfgram_cli.enums import LevelsEnum


class ReloadHandler(watchdog.events.FileSystemEventHandler):
    """
    Handles file system events to trigger a bot reload.

    This class monitors for modifications to Python files within
    a specified directory. When file is modified, it
    logs the event and reloads the bot using `os.execl`.
    """

    def __init__(self, bot: "Bot"):
        """
        Initializes the ReloadHandler.

        Args:
            bot: The bot instance to reload.
        """
        self.bot = bot

    def on_modified(self, event: watchdog.events.FileSystemEvent) -> None:
        """
        Handles file modification events.

        This method is called when a file is modified within the monitored directory.
        It checks if the modified file and, if so, triggers a bot reload.

        Args:
            event: The file system event object.
        """
        debugger.log(
            f"File '{event.src_path}' has been modified. Reloading...",
            LevelsEnum.INFO,
        )
        self.reload_bot()

    def reload_bot(self) -> None:
        """
        Reloads the bot.
        """
        os.execl(sys.executable, sys.executable, *sys.argv)


def monitor_changes(bot: "Bot", directory: str) -> None:
    """
    Monitors a directory for changes and reloads the bot upon file modifications.

    This function sets up a file system observer using the `watchdog` library.
    It monitors the specified directory recursively for changes, and when a Python
    file is modified, it triggers a bot reload.  It runs until interrupted by a
    keyboard interrupt.

    Args:
        bot: The bot instance to monitor and reload.
        directory: The directory to monitor for file changes.
    """
    event_handler = ReloadHandler(bot)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        debugger.log("File monitoring stopped.", LevelsEnum.INFO)
        observer.stop()
    observer.join()
