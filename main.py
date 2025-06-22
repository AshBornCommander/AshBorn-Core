# main.py  – AshBorn core launcher
from dotenv import load_dotenv
from loguru import logger
import os, threading, asyncio
from datetime import datetime

# ── Optional colour output ─────────────────────────
try:
    from colorama import Fore, Style
except ImportError:          # safe fallback if colorama missing
    class Dummy:             # noqa
        def __getattr__(self, _): return ""
    Fore = Style = Dummy()
# ───────────────────────────────────────────────────

from bot.realtime      import watch_command_file          # 🔁 local command.txt watcher
from bot.telegram_bot  import start_telegram_bot          # 📲 Telegram listener
from bot.alpha_sniffer import start_sniffer_loop          # 🔎 Solana token watcher

# ── ENV ─────────────────────────────────────────────
load_dotenv()
BOT_NAME  = os.getenv("BOT_NAME", "AshBorn")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# ────────────────────────────────────────────────────

# ── Logger ──────────────────────────────────────────
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)
# ────────────────────────────────────────────────────

def _start_telegram_thread() -> None:
    """Runs Telegram polling in its own daemon thread."""
    threading.Thread(
        target=start_telegram_bot,
        name="TelegramThread",
        daemon=True
    ).start()

def _start_sniffer_thread() -> None:
    """Runs the async alpha-sniffer loop in its own daemon thread."""
    def _runner() -> None:
        asyncio.run(start_sniffer_loop())     # infinite async loop
    threading.Thread(
        target=_runner,
        name="SnifferThread",
        daemon=True
    ).start()

def main() -> None:
    """AshBorn boot sequence."""
    logger.info(
        Fore.CYAN +
        f"\n🤖 [{BOT_NAME}] is waking up at {datetime.now().isoformat()} …\n" +
        Style.RESET_ALL
    )

    # 1️⃣  Telegram remote-control interface
    _start_telegram_thread()

    # 2️⃣  Alpha-Sniffer (Solana new-token detector)
    _start_sniffer_thread()

    # 3️⃣  Local command-file watcher (blocks forever)
    watch_command_file()                     # <— continuous loop

# ── Entry-point guard ──────────────────────────────
if __name__ == "__main__":
    main()
