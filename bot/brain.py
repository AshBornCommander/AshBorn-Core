# bot/brain.py
"""
AshBorn “Brain” – central command router + alpha-event promoter
────────────────────────────────────────────────────────────────
Phase-0  = simulation only
  • BUY / SELL → fake buyer
  • STATUS / REBALANCE → log only
  • Alpha-events come from sniffer → auto-promoted to BUY

Later you can:
  • swap simulate_buy() for real DEX calls
  • plug risk-management filters
  • push receipts to Telegram, DB, etc.
"""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from typing import Deque, Dict, Tuple

from loguru import logger

from bot.buyer import simulate_buy  # fake BUY helper for now

# ────────────────────────── Alpha queue ────────────────────────────
# alpha_sniffer will call push_alpha_event(symbol, name)
ALPHA_QUEUE: Deque[Dict[str, str]] = deque()


def push_alpha_event(symbol: str, name: str) -> None:
    """
    Called from alpha_sniffer whenever a *fresh* pool is detected.
    We enqueue a tiny dict; the brain will decide what to do.
    """
    ALPHA_QUEUE.append(
        {
            "symbol": symbol.upper(),
            "name": name,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
    )
    logger.debug(f"➕  Alpha event queued → {symbol}/{name}")


# ─────────────────────── brain “manager” class ─────────────────────
class CommandBrain:
    """
    High-level coordinator that:

      1. Watches ALPHA_QUEUE for new token events
      2. Deduplicates by (symbol, ts)
      3. Converts each *new* event to a BUY command (simulated for now)
      4. Hands the BUY off to handle_command()

    You can run its loop in the background:

        brain = CommandBrain()
        asyncio.create_task(brain.alpha_watcher_loop())
    """

    def __init__(self) -> None:
        self.seen: set[Tuple[str, str]] = set()  # (symbol, ts)

    async def alpha_watcher_loop(self, poll: int = 5) -> None:
        """Async loop: drain the queue every *poll* seconds."""
        logger.info("🧠 Alpha-watcher loop spun-up …")
        while True:
            self.analyze_alpha()
            await asyncio.sleep(poll)

    def analyze_alpha(self) -> None:
        """Process all queued alpha events (non-blocking)."""
        processed = 0
        while ALPHA_QUEUE:
            evt = ALPHA_QUEUE.popleft()
            key = (evt["symbol"], evt["ts"])
            if key in self.seen:
                continue  # duplicate
            self.seen.add(key)
            processed += 1

            cmd = {
                "action": "BUY",
                "token": evt["symbol"],
                "amount": 0.20,  # default snipe size (SOL) – tweak later
            }
            logger.info(f"🧠 Promoting alpha ⇒ BUY → {cmd}")
            handle_command(cmd)

        if processed:
            logger.debug(f"🧠 AlphaBrain processed {processed} event(s).")


# ───────────────────────── command router ──────────────────────────
def handle_command(cmd: dict | str) -> None:
    """
    Execute a parsed command.

    Accepts either:
      • dict – {"action": "BUY", "token": "SOL", "amount": 0.2}
      • str  – legacy shorthand ("BUY", "SELL", …)
    """
    if isinstance(cmd, str):
        cmd = {"action": cmd.upper()}

    action = (cmd.get("action") or "").upper()
    token = cmd.get("token")
    amount = cmd.get("amount")

    # BUY ──────────────────────────────────────────────────────────
    if action == "BUY":
        logger.info(f"🚀 BUY signal → token={token} amount={amount}")
        receipt = simulate_buy(token or "UNKNOWN", amount or 0.0)
        logger.success(f"🧾 Fake-buy receipt → {receipt}")
        return

    # SELL ─────────────────────────────────────────────────────────
    if action == "SELL":
        logger.info(f"💸 SELL signal → token={token} amount={amount}")
        logger.warning("⚠️  SELL simulation not implemented yet")
        return

    # STATUS ───────────────────────────────────────────────────────
    if action == "STATUS":
        logger.info("📊 STATUS check requested")
        # TODO: fetch balances / PnL and reply
        return

    # REBALANCE ────────────────────────────────────────────────────
    if action == "REBALANCE":
        logger.info("⚖️ Portfolio rebalance requested")
        # TODO: run rebalancing algorithm
        return

    # Unknown  ─────────────────────────────────────────────────────
    logger.warning(f"🤷‍♂️ Unknown command: {cmd}")


# ─────────────────────── helper for main.py ────────────────────────
def launch_background_tasks(loop: asyncio.AbstractEventLoop | None = None) -> None:
    """
    Convenience: call from main.py to spin the alpha-watcher
    alongside your other async services.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    brain = CommandBrain()
    loop.create_task(brain.alpha_watcher_loop())


# Quick self-test when run directly
if __name__ == "__main__":
    push_alpha_event("TEST", "DemoToken")
    CommandBrain().analyze_alpha()
