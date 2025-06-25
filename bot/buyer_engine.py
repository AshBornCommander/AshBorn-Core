# bot/buyer_engine.py – Simulated token buying engine (placeholder for real trades)

from loguru import logger
from datetime import datetime
import random

def simulate_buy_token(symbol: str, amount: float) -> dict:
    """
    Simulates a token purchase and returns a fake receipt.

    Arguments:
    - symbol: Token symbol (e.g. SOL, PEPEKING)
    - amount: Amount of token to 'buy'

    Returns:
    - A dict receipt with fake transaction details
    """
    price = round(random.uniform(0.01, 5.00), 4)   # Fake price per token
    total_cost = round(amount * price, 4)

    receipt = {
        "token": symbol.upper(),
        "amount": amount,
        "price": price,
        "total_cost": total_cost,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    logger.info(f"💰 Simulated BUY: {amount} {symbol.upper()} @ ${price} each → total ${total_cost}")
    return receipt
