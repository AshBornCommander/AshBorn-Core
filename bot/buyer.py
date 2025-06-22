# bot/buyer.py – Simulated token purchase handler for AshBorn

from loguru import logger
from datetime import datetime

def simulate_buy(token: str, amount: float) -> dict:
    """
    Simulate buying a token. Replace this later with real wallet logic.
    """
    logger.info(f"💰 Simulating buy: {amount} SOL into {token}")

    fake_txn = {
        "token": token,
        "amount": amount,
        "price": 0.000123,  # random dummy price
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "success",
        "tx_hash": "SIMULATED1234567890"
    }

    logger.success(f"✅ Fake buy completed: {fake_txn['tx_hash']}")
    return fake_txn
