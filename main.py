# main.py
from dotenv import load_dotenv
from loguru import logger
import os
from datetime import datetime

# ── Optional colour output ─────────────────────────
try:
    from colorama import Fore, Style
except ImportError:
    # If colorama isn't installed, fall back to plain text
    class Dummy:
        def __getattr__(self, item):  # noqa
            return ""
    Fore = Style = Dummy()
# ───────────────────────────────────────────────────

from bot.commands import parse_command
from bot.brain import handle_command        # 🧠 AshBorn's command brain
from bot.realtime import watch_command_file # 🔁 Live command monitor

# ── Load environment variables ─────────────────────
load_dotenv()

BOT_NAME  = os.getenv("BOT_NAME", "AshBorn")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# ───────────────────────────────────────────────────

# ── Configure logger ───────────────────────────────
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)
# ───────────────────────────────────────────────────

def main() -> None:
    """Boot sequence for AshBorn."""
    logger.info(
        Fore.CYAN
        + f"\n🤖 [{BOT_NAME}] is waking up at {datetime.now().isoformat()} …\n"
        + Style.RESET_ALL
    )

    # Start watching the command.txt file for real-time commands
    watch_command_file()                     # <— continuous loop

# ── Entry-point guard ──────────────────────────────
if __name__ == "__main__":
    main()
