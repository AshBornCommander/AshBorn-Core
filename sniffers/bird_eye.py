# bird_eye.py

import os
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# ✅ Load API Key
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
if not BIRDEYE_API_KEY:
    raise RuntimeError("❌ Missing BIRDEYE_API_KEY in .env file")

# ✅ Endpoints
TOKENLIST_API = "https://public-api.birdeye.so/defi/tokenlist"
PRICE_API = "https://public-api.birdeye.so/defi/price"

# ✅ Auth headers
HEADERS = {
    "accept": "application/json",
    "X-API-KEY": BIRDEYE_API_KEY,
}

def fetch_latest_tokens(limit: int = 10) -> list[dict]:
    """Fetch latest Solana tokens from BirdEye and filter/sort manually by volume."""
    try:
        params = {
            "chain": "solana"
        }
        response = requests.get(TOKENLIST_API, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # ✅ Extract tokens list correctly from nested structure
        if not data or "data" not in data or "tokens" not in data["data"]:
            logger.warning("⚠️ BirdEye returned unexpected format for token data.")
            return []

        all_tokens = data["data"]["tokens"]

        # ✅ Filter by mcap and liquidity
        filtered = [
            t for t in all_tokens
            if t.get("mc", 0) > 10_000 and t.get("liquidity", 0) > 10_000
        ]

        # ✅ Sort manually by volume_24h_usd (desc)
        sorted_tokens = sorted(filtered, key=lambda x: x.get("volume_24h_usd", 0), reverse=True)

        logger.debug(f"📡 BirdEye fetched and sorted {len(sorted_tokens)} tokens")
        return sorted_tokens[:limit]

    except Exception as e:
        logger.error(f"❌ Error fetching BirdEye tokens: {e}")
        return []

def fetch_token_price(token_address: str) -> float:
    """Fetch token price from BirdEye."""
    try:
        params = {"address": token_address}
        response = requests.get(PRICE_API, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data.get("data", {}).get("value", 0.0))
    except Exception as e:
        logger.error(f"❌ Error fetching price for {token_address}: {e}")
        return 0.0
