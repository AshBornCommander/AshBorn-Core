# main.py  – AshBorn core launcher

import os, threading, asyncio
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger

# ── Optional colour output ─────────────────────────
try:
    from colorama import Fore, Style
except ImportError:          # safe fallback if colorama missing
    class Dummy:
        def __getattr__(self, _):  # noqa
            return ""
    Fore = Style = Dummy()
# ───────────────────────────────────────────────────

from bot.realtime      import watch_command_file          # 🔁 command.txt watcher
from bot.telegram_bot  import start_telegram_bot          # 📲 Telegram listener
from bot.alpha_sniffer import start_sniffer_loop          # 🔎 Solana token watcher
from bot.brain         import launch_background_tasks     # 🧠 Alpha-Brain loop

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
    """
    Runs the async alpha-sniffer loop in its own daemon thread
    *and* schedules the Brain’s alpha-watcher on the same loop.
    """
    def _runner() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # ── 🧠 Schedule Brain watcher on this loop ──
        launch_background_tasks(loop)

        # ── 🔎 Run sniffer loop forever ─────────────
        loop.run_until_complete(start_sniffer_loop())

    threading.Thread(
        target=_runner,
        name="SnifferThread",
        daemon=True
    ).start()


def main() -> None:
    """AshBorn boot sequence."""
    logger.info(
        Fore.CYAN
        + f"\n🤖 [{BOT_NAME}] is waking up at {datetime.now().isoformat()} …\n"
        + Style.RESET_ALL
    )

    # 1️⃣  Telegram remote-control interface
    _start_telegram_thread()

    # 2️⃣  Alpha-Sniffer + Brain alpha-watcher
    _start_sniffer_thread()

    # 3️⃣  Local command-file watcher (blocks forever)
    watch_command_file()   # <— continuous loop


# ── Entry-point guard ──────────────────────────────
if __name__ == "__main__":
    main()
