# bot/brain.py
"""
AshBorn’s ‘brain’ – where trading logic lives.
Right now it only logs what it would do.  Later you can
  • call a real DEX / CEX SDK
  • enqueue tasks
  • run risk checks, etc.
"""

from loguru import logger

# ------------------------------------------------------------------
def handle_command(cmd: dict | str) -> None:
    """
    Execute a parsed command.

    Accepts:
      • dict  – {'action': 'BUY', 'token': 'SOL', 'amount': 0.2}
      • str   – legacy support ("BUY", "SELL", …)
    """
    # ── Back-compat: allow plain strings ───────────────────────────
    if isinstance(cmd, str):
        cmd = {"action": cmd.upper()}

    action = cmd.get("action")
    token  = cmd.get("token")
    amount = cmd.get("amount")

    # ── BUY ────────────────────────────────────────────────────────
    if action == "BUY":
        logger.info(f"🚀 BUY signal → token={token} amount={amount}")
        # TODO: insert real buy logic here
        return

    # ── SELL ───────────────────────────────────────────────────────
    if action == "SELL":
        logger.info(f"💸 SELL signal → token={token} amount={amount}")
        # TODO: insert real sell logic here
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

    # ── Unknown ----------------------------------------------------
    logger.warning(f"🤷‍♂️ No valid operation mapped for command: {cmd}")
