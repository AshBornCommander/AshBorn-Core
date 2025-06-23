import requests
from loguru import logger
from datetime import datetime, timedelta

BIRDEYE_API = "https://public-api.birdeye.so/public/token/price"
NEW_LISTINGS_API = "https://public-api.birdeye.so/public/token/updated"
BIRDEYE_HEADERS = {
    "accept": "application/json",
    "x-chain": "solana",
}

def fetch_latest_tokens(minutes=3):
    """Fetch recently listed Solana tokens in last N minutes"""
    try:
        now = datetime.utcnow()
        past_time = now - timedelta(minutes=minutes)
        past_timestamp = int(past_time.timestamp())

        response = requests.get(
            f"{NEW_LISTINGS_API}?time={past_timestamp}",
            headers=BIRDEYE_HEADERS
        )
        response.raise_for_status()
        data = response.json()

        if not data or "data" not in data:
            logger.warning("No token data found from BirdEye.")
            return []

        return data["data"]

    except Exception as e:
        logger.error(f"Error fetching BirdEye tokens: {e}")
        return []
