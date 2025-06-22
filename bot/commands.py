# bot/commands.py

from loguru import logger

def parse_command(input_text: str) -> dict | None:
    """
    Parse commands like:
    - 'buy SOL 0.2'
    - 'sell DOGE'
    - 'status'
    
    Returns:
    - {'action': 'BUY', 'token': 'SOL', 'amount': 0.2}
    - {'action': 'STATUS'}
    """
    input_text = input_text.strip().lower()
    parts = input_text.split()

    if not parts:
        logger.warning("🧠 Empty command.")
        return None

    command = parts[0]

    if command == "buy":
        logger.info("🧠 Detected command: BUY")
        return {
            "action": "BUY",
            "token": parts[1].upper() if len(parts) > 1 else None,
            "amount": float(parts[2]) if len(parts) > 2 else None
        }

    elif command == "sell":
        logger.info("🧠 Detected command: SELL")
        return {
            "action": "SELL",
            "token": parts[1].upper() if len(parts) > 1 else None,
            "amount": float(parts[2]) if len(parts) > 2 else None
        }

    elif command == "status":
        logger.info("🧠 Detected command: STATUS")
        return {"action": "STATUS"}

    elif command == "rebalance":
        logger.info("🧠 Detected command: REBALANCE")
        return {"action": "REBALANCE"}

    else:
        logger.warning("🧠 Command not recognized.")
        return None
