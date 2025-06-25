# sniffers/alpha_sniffer.py

import asyncio
import time
from sniffers.bird_eye import fetch_latest_tokens
from bot.brain import push_alpha_event

# Track seen token addresses to avoid duplicates
seen_symbols = set()

async def start_sniffer_loop(poll: int = 60):
    """Periodically pull fresh tokens from BirdEye and push as alpha events."""
    while True:
        print("🔎 Sniffer: Fetching new tokens from BirdEye...")
        try:
            tokens = fetch_latest_tokens(limit=15)

            for token in tokens:
                symbol = token.get("symbol")
                name = token.get("name")

                if not symbol or not name:
                    continue
                if symbol in seen_symbols:
                    continue

                seen_symbols.add(symbol)
                print(f"[ALPHA] New Token Detected: {symbol} / {name}")
                push_alpha_event(symbol, name)

        except Exception as e:
            print(f"⚠️ Sniffer error: {e}")

        await asyncio.sleep(poll)

# For manual testing
if __name__ == "__main__":
    asyncio.run(start_sniffer_loop())
