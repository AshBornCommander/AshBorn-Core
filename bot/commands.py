# bot/commands.py

from loguru import logger

def parse_command(input_text: str) -> str:
    input_text = input_text.strip().lower()

    if "buy" in input_text:
        logger.info("🧠 Detected command: BUY")
        return "BUY"
    elif "sell" in input_text:
        logger.info("🧠 Detected command: SELL")
        return "SELL"
    elif "status" in input_text:
        logger.info("🧠 Detected command: STATUS")
        return "STATUS"
    elif "rebalance" in input_text:
        logger.info("🧠 Detected command: REBALANCE")
        return "REBALANCE"
    else:
        logger.warning("🧠 Command not recognized.")
        return "UNKNOWN"

 
