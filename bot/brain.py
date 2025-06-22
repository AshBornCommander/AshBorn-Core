# bot/brain.py
"""
AshBorn’s ‘brain’ – where trading logic lives.
Phase I = simulation only.  
  • BUY / SELL call the fake buyer  
  • STATUS / REBALANCE just log actions

Later you can:
  • call a real DEX / CEX SDK
  • run risk-management checks
  • push Telegram receipts, etc.
"""

from loguru import logger
from bot.buyer import simulate_buy             # ← new fake-buy helper
# (there is no simulate_sell yet – we’ll add that later)

# ────────────────────────────────────────────────────────────────────
def handle_command(cmd: dict | str) -> None:
    """
    Execute a parsed command.

    Accepts either:
      • dict  – {"action": "BUY", "token": "SOL", "amount": 0.2}
      • str   – legacy support ("BUY", "SELL", …)
    """
    # ── Back-compat: allow plain strings ───────────────────────────
    if isinstance(cmd, str):
        cmd = {"action": cmd.upper()}

    action = (cmd.get("action") or "").upper()
    token  = cmd.get("token")
    amount = cmd.get("amount")

    # ── BUY ────────────────────────────────────────────────────────
    if action == "BUY":
        logger.info(f"🚀 BUY signal → token={token} amount={amount}")
        receipt = simulate_buy(token or "UNKNOWN", amount or 0.0)
        logger.success(f"🧾  Fake-buy receipt → {receipt}")
        return

    # ── SELL ───────────────────────────────────────────────────────
    if action == "SELL":
        logger.info(f"💸 SELL signal → token={token} amount={amount}")
        logger.warning("⚠️  SELL simulation not implemented yet")
        return

    # ── STATUS ─────────────────────────────────────────────────────
    if action == "STATUS":
        logger.info("📊 STATUS check requested")
        # TODO: fetch balances / PnL and reply
        return

    # ── REBALANCE ─────────────────────────────────────────────────
    if action == "REBALANCE":
        logger.info("⚖️ Portfolio rebalance requested")
        # TODO: run rebalancing algorithm
        return

    # ── Unknown command ───────────────────────────────────────────
    logger.warning(f"🤷‍♂️  No valid operation mapped for command: {cmd}")
