# main.py

from dotenv import load_dotenv
from loguru import logger
import os
from datetime import datetime
from bot.commands import parse_command
from bot.brain import handle_command  # 🧠 AshBorn's command brain

# Load environment variables
load_dotenv()

BOT_NAME = os.getenv("BOT_NAME", "AshBorn")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logger
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)

def main():
    logger.info(f"\n🤖 [{BOT_NAME}] is waking up at {datetime.now().isoformat()}\n")

    # Simulated incoming command message
    raw_message = "buy SOL now"  # 🔮 This can later be fed from Telegram, Discord, etc.
    command = parse_command(raw_message)

    if command:
        logger.info(f"🚀 Executing action for command: {command}")
        handle_command(command)  # 🧠 pass it to the command brain
    else:
        logger.info("🕵️ No actionable command found.")

if __name__ == "__main__":
    main()
