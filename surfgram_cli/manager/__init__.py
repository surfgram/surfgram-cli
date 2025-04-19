import os
import shutil
import sys
import importlib
import inspect
import threading
from pathlib import Path
from typing import Optional, Tuple
from jinja2 import Environment, FileSystemLoader
from surfgram import configs as surfgram_configs
from surfgram_cli.utils import monitor_changes, debugger
from surfgram_cli.cli import console

class BotManager:
    """Bot management core functionality"""

    @staticmethod
    def create_bot(bot_name: str, token: str) -> bool:
        """Creates a bot structure from templates."""
        templates_dir = Path(__file__).parent.parent / "templates" / "bot_structure"
        if not templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

        env = Environment(loader=FileSystemLoader(templates_dir))
        bot_path = Path(bot_name)

        if bot_path.exists():
            if console.prompt(f"Directory '{bot_name}' exists. Overwrite? (y/N): ").lower() != 'y':
                return False
            shutil.rmtree(bot_path)

        bot_path.mkdir()
        for template in env.list_templates():
            output = bot_path / template.replace(".j2", "")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(env.get_template(template).render(bot_name=bot_name, token=token))
        return True

    @staticmethod
    def delete_bot(bot_name: str) -> None:
        """Deletes a bot directory."""
        path = Path(bot_name)
        if not path.exists():
            raise FileNotFoundError(f"Bot directory '{bot_name}' not found")
        shutil.rmtree(path)

    @staticmethod
    def find_config(bot_dir: Optional[str] = None) -> str:
        """Finds and validates the bot config class."""
        target_dir = Path(bot_dir) if bot_dir else Path.cwd()
        target_dir = target_dir.resolve()

        if not target_dir.exists():
            raise FileNotFoundError(f"Directory not found: {target_dir}")

        if not (target_dir / "__init__.py").exists():
            raise ImportError(
                f"Directory '{target_dir.name}' is not a Python package\n"
                f"Solution: Add __init__.py file to make it a proper package"
            )

        sys.path.insert(0, str(target_dir.parent))
        module_name = target_dir.name

        try:
            bot_module = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            if e.name == module_name:
                raise ImportError(
                    f"Failed to import '{module_name}'\n"
                    f"Possible causes:\n"
                    f"1. Missing __init__.py\n"
                    f"2. Incorrect Python package structure"
                ) from e
            raise ImportError(f"Missing dependency: {e.name}\nFix: pip install {e.name}") from e

        config_classes = [
            name for name, cls in inspect.getmembers(bot_module, inspect.isclass)
            if isinstance(cls, type) 
            and issubclass(cls, surfgram_configs.BaseConfig) 
            and cls != surfgram_configs.BaseConfig
        ]

        if not config_classes:
            raise AttributeError(
                f"No valid config classes found in {module_name}\n"
                f"Requirements:\n"
                f"1. Must inherit from surfgram.configs.BaseConfig\n"
                f"2. Must be imported in {module_name}/__init__.py"
            )

        if len(config_classes) == 1:
            return f"{module_name}.{config_classes[0]}"

        console.print_cancel(f"Multiple configs found in {module_name}:")
        for i, name in enumerate(config_classes, 1):
            console.print_cancel(f"{i}. {module_name}.{name}")
        
        choice = console.prompt("Select config (number)")
        try:
            return f"{module_name}.{config_classes[int(choice)-1]}"
        except (ValueError, IndexError) as e:
            raise ValueError("Invalid selection. Please enter a valid number.") from e

    @staticmethod
    def _parse_config(config: str) -> Tuple[str, str]:
        """Splits config path into module and class name."""
        if not isinstance(config, str) or "." not in config:
            raise ValueError(
                f"Invalid config format: '{config}'\n"
                f"Expected format: 'module_name.ClassName'"
            )
        return config.rsplit(".", 1)

    @staticmethod
    def _validate_config_class(module, class_name: str) -> type:
        """Validates that the config class exists and is correct."""
        if not hasattr(module, class_name):
            available = [n for n, _ in inspect.getmembers(module, inspect.isclass)]
            raise AttributeError(
                f"Class '{class_name}' not found in '{module.__name__}'\n"
                f"Available classes: {', '.join(available)}"
            )
        config_class = getattr(module, class_name)
        if not isinstance(config_class, type):
            raise AttributeError(f"'{class_name}' is not a class")
        return config_class

    @staticmethod
    def _cast_config_values(config_instance) -> None:
        """Auto-casts string numbers to int/float in config."""
        for field, value in vars(config_instance).items():
            if isinstance(value, str):
                if value.isdigit():
                    setattr(config_instance, field, int(value))
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                    setattr(config_instance, field, float(value))

    @staticmethod
    def run_bot(bot: str, config: str, debug: bool, on_reload: bool) -> None:
        """Runs the bot with the given configuration."""
        from surfgram.core.bot import Bot

        bot_dir = Path(bot).resolve() if bot != "." else Path.cwd()
        if not bot_dir.exists():
            raise FileNotFoundError(f"Bot directory not found: {bot_dir}")

        sys.path.insert(0, str(bot_dir.parent))

        try:
            module_name, class_name = BotManager._parse_config(config)
            module = importlib.import_module(module_name)
            config_class = BotManager._validate_config_class(module, class_name)
            
            temp_config = config_class()
            BotManager._cast_config_values(temp_config)
            
        except ModuleNotFoundError as e:
            if e.name == module_name:
                raise ImportError(
                    f"Module '{module_name}' not found\n"
                    f"Check:\n"
                    f"1. Is '{bot_dir.name}' a proper Python package?\n"
                    f"2. Is the package in correct location?"
                ) from e
            raise
            
        debugger.debug_mode = debug
        bot_instance = Bot(config=config_class)

        if on_reload:
            threading.Thread(
                target=monitor_changes,
                args=(bot_instance, str(bot_dir)),
                daemon=True
            ).start()

        bot_instance.listen()