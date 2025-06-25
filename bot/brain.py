# bot/brain.py
"""
AshBorn “Brain” – central command router + alpha-event promoter
────────────────────────────────────────────────────────────
Phase-0  = simulation only
  • BUY / SELL → fake buyer_engine
  • STATUS / REBALANCE → log only
  • Alpha events come from sniffer → auto-promoted to BUY

Later you can:
  • swap simulate_buy_token() for real DEX calls
  • plug risk-management filters
  • push Telegram receipts, DB writes, etc.
"""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from typing import Deque, Dict, Tuple

from loguru import logger
from bot.buyer_engine import simulate_buy_token
from sniffers.bird_eye import fetch_latest_tokens  # ✅ New import

# ─────────────────── Alpha queue ───────────────────
ALPHA_QUEUE: Deque[Dict[str, str]] = deque()


def push_alpha_event(symbol: str, name: str) -> None:
    ALPHA_QUEUE.append({
        "symbol": symbol.upper(),
        "name": name,
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    logger.debug(f"➕ Alpha event queued → {symbol}/{name}")


# ─────────────── brain “manager” class ───────────────
class CommandBrain:
    def __init__(self) -> None:
        self.seen: set[Tuple[str, str]] = set()

    async def alpha_watcher_loop(self, poll: int = 5) -> None:
        logger.info("🧠 Alpha-watcher loop spun-up …")
        while True:
            self.analyze_alpha()
            await asyncio.sleep(poll)

    def analyze_alpha(self) -> None:
        processed = 0
        while ALPHA_QUEUE:
            evt = ALPHA_QUEUE.popleft()
            key = (evt["symbol"], evt["ts"])
            if key in self.seen:
                continue
            self.seen.add(key)
            processed += 1

            cmd = {
                "action": "BUY",
                "token": evt["symbol"],
                "amount": 0.20,
            }
            logger.info(f"🧠 Promoting alpha ⇒ BUY → {cmd}")
            handle_command(cmd)

        if processed:
            logger.debug(f"🧠 AlphaBrain processed {processed} event(s).")

    def simulate_birdeye_trades(self) -> None:
        logger.info("📡 Checking BirdEye for fresh tokens …")
        tokens = fetch_latest_tokens(limit=10)
        shortlisted = []

        for t in tokens:
            try:
                if t.get("liquidity", 0) < 10_000:
                    continue
                if t.get("volume_24h_usd", 0) < 50_000:
                    continue
                if not t.get("name") or not t.get("symbol"):
                    continue
                if any(x in t["name"].lower() for x in ["test", "fake", "scam"]):
                    continue
                shortlisted.append(t)
            except Exception as e:
                logger.warning(f"⚠️ Token parse error: {e}")

        for token in shortlisted:
            cmd = {
                "action": "BUY",
                "token": token["symbol"],
                "amount": 0.20,
            }
            logger.info(f"🧠 [BirdEye] Promoting filtered ⇒ BUY → {cmd}")
            handle_command(cmd)


# ─────────────── command router ───────────────
def handle_command(cmd: dict | str) -> None:
    if isinstance(cmd, str):
        cmd = {"action": cmd.upper()}

    action = (cmd.get("action") or "").upper()
    token = cmd.get("token")
    amount = cmd.get("amount")

    if action == "BUY":
        logger.info(f"🚀 BUY signal → token={token} amount={amount}")
        receipt = simulate_buy_token(token or "UNKNOWN", amount or 0.0)
        logger.success(f"📟 Fake-buy receipt → {receipt}")
        return

    if action == "SELL":
        logger.info(f"💸 SELL signal → token={token} amount={amount}")
        logger.warning("⚠️ SELL simulation not implemented yet")
        return

    if action == "STATUS":
        logger.info("📊 STATUS check requested")
        # TODO
        return

    if action == "REBALANCE":
        logger.info("⚖️ Portfolio rebalance requested")
        # TODO
        return

    logger.warning(f"🤷‍♂️ Unknown command: {cmd}")


# ───────── helper to launch watcher ─────────
def launch_background_tasks(loop: asyncio.AbstractEventLoop | None = None) -> None:
    if loop is None:
        loop = asyncio.get_event_loop()
    brain = CommandBrain()
    loop.create_task(brain.alpha_watcher_loop())


# ───────── quick self-test ─────────
if __name__ == "__main__":
    push_alpha_event("TEST", "DemoToken")
    brain = CommandBrain()
    brain.analyze_alpha()
    brain.simulate_birdeye_trades()  # ✅ Manual BirdEye trigger
