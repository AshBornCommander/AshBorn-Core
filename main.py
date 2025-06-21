# main.py

from dotenv import load_dotenv
from loguru import logger
import os
from datetime import datetime

# Load environment variables
load_dotenv()

BOT_NAME = os.getenv("BOT_NAME", "AshBorn")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logger
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)

def main():
    logger.info(f"\n🤖 [{BOT_NAME}] is waking up at {datetime.now().isoformat()}\n")

if __name__ == "__main__":
    main()
