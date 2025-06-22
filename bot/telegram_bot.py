# bot/telegram_bot.py  – compatible with python-telegram-bot 20.x+
# Adds:  • full-dict commands  • error-resistant auto-reconnect loop

import os, asyncio, time, traceback
from loguru import logger
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.commands import parse_command
from bot.brain    import handle_command          # now expects the *dict* from parse_command

# ────────────────────────── ENV ────────────────────────────────
load_dotenv()
TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))
# ───────────────────────────────────────────────────────────────


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle every text message sent to the bot."""
    try:
        msg_text = (update.message.text or "").strip()
        user_id  = update.effective_user.id

        # ─── owner-only guard ───────────────────────────────────
        if user_id != CHAT_ID:
            logger.warning("❌  Unauthorized user tried to send command.")
            await update.message.reply_text(
                "🚫  Sorry, you’re not allowed to control AshBorn."
            )
            return

        logger.info(f"📩  Received Telegram message: {msg_text}")

        cmd = parse_command(msg_text)                              # ← returns dict
        if cmd["action"] == "UNKNOWN":
            await update.message.reply_text(
                "🤷‍♂️  Unknown command. Try e.g.:\n"
                "`buy SOL 0.2`\n`sell DOGE 1.0`\n`status`\n`rebalance`",
                parse_mode="Markdown",
            )
            return

        # ─── Human-friendly acknowledgement ────────────────────
        token_txt  = f" {cmd.get('token','')}" if cmd.get("token") else ""
        amount_txt = f" {cmd['amount']}"       if cmd.get("amount") is not None else ""
        await update.message.reply_text(
            f"🛠  AshBorn accepted **{cmd['action']}{token_txt}{amount_txt}**",
            parse_mode="Markdown",
        )

        # ─── Pass FULL dict into trading brain ──────────────────
        logger.info(f"🚀  Executing Telegram command: {cmd}")
        handle_command(cmd)

    except Exception as exc:
        logger.error(f"❌  Telegram handler error: {exc}\n{traceback.format_exc()}")
        await update.message.reply_text("⚠️  Internal error while processing command.")


# ─────────────────────────── POLLER ────────────────────────────
def _run_polling() -> None:
    """Start a single polling session (may raise)."""
    asyncio.set_event_loop(asyncio.new_event_loop())       # each thread needs its own loop
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    logger.info("🤖  Telegram bot polling has started …")
    app.run_polling()                                      # blocking until error / ^C


def start_telegram_bot() -> None:
    """Start Telegram polling in a background thread, with auto-reconnect."""
    if not TOKEN:
        logger.error("⚠️  TELEGRAM_BOT_TOKEN missing in .env")
        return

    while True:                                            # auto-reconnect loop
        try:
            _run_polling()                                 # returns only on fatal error / ^C
        except Exception as exc:
            logger.warning(f"🔁  Telegram bot disconnected: {exc!r}")
            logger.info("♻️  Reconnecting in 5 s …")
            time.sleep(5)
