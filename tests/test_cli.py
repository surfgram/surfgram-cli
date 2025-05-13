import pytest
from unittest.mock import MagicMock
from surfgram_cli import app


class TestSurfgramCLI:

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        # Mock ConsoleComponent
        self.console_mock = MagicMock()
        monkeypatch.setattr("surfgram_cli.ConsoleComponent", lambda: self.console_mock)

        # Mock BotManager
        self.bot_manager_mock = MagicMock()
        monkeypatch.setattr("surfgram_cli.manager.BotManager", self.bot_manager_mock)

    def test_callback_no_graphics(self):
        """Test the callback with graphics enabled"""
        app.invoke(app.callback, no_graphics=False)
        self.console_mock.set_status.assert_called_once_with(graphics=True)

    def test_callback_graphics_disabled(self):
        """Test the callback with graphics disabled"""
        app.invoke(app.callback, no_graphics=True)
        self.console_mock.set_status.assert_not_called()

    def test_new_bot_creation_success(self):
        """Test successful bot creation"""
        self.console_mock.prompt.return_value = "dummy_token"
        self.bot_manager_mock.create_bot.return_value = True

        result = app.invoke(app.new, bot_name="TestBot", types="all")
        assert result.exit_code == 0
        self.console_mock.print_success_message.assert_called_once_with(
            "✨ Bot 'TestBot' created successfully!\n"
            "📁 Project structure initialized\n"
            "🚀 Ready to listen!"
        )

    def test_new_bot_creation_canceled(self):
        """Test bot creation canceled"""
        self.console_mock.prompt.return_value = "dummy_token"
        self.bot_manager_mock.create_bot.return_value = False

        result = app.invoke(app.new, bot_name="TestBot", types="commands")
        assert result.exit_code == 0
        self.console_mock.print_cancel.assert_called_once_with("Bot creation cancelled")

    def test_delete_bot_confirmation(self):
        """Test deletion of a bot after confirmation"""
        self.console_mock.confirm.return_value = True

        result = app.invoke(app.delete, bot_name="TestBot")
        assert result.exit_code == 0
        self.bot_manager_mock.delete_bot.assert_called_once_with("TestBot")
        self.console_mock.print_success_message.assert_called_once_with(
            "✅ Bot 'TestBot' has been deleted"
        )

    def test_delete_bot_canceled(self):
        """Test deletion of a bot when canceled"""
        self.console_mock.confirm.return_value = False

        result = app.invoke(app.delete, bot_name="TestBot")
        assert result.exit_code == 0
        self.bot_manager_mock.delete_bot.assert_not_called()
        self.console_mock.print_cancel.assert_called_once_with("Deletion cancelled.")

    def test_run_bot(self):
        """Test running of a bot"""
        self.bot_manager_mock.run_bot.return_value = None
        result = app.invoke(
            app.run, bot="TestBotDir", config="TestConfigClass", debug=True
        )
        assert result.exit_code == 0
        self.bot_manager_mock.run_bot.assert_called_once_with(
            "TestBotDir", "TestBotDir.TestConfigClass", True, False
        )
