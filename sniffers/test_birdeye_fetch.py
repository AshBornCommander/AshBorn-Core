# sniffers/test_birdeye_fetch.py

from bird_eye import fetch_latest_tokens
from pprint import pprint

if __name__ == "__main__":
    print("🔍 Fetching latest Solana tokens from BirdEye...\n")
    tokens = fetch_latest_tokens(limit=5)

    if not tokens:
        print("❌ FAILED: No tokens returned.")
    else:
        print(f"✅ SUCCESS: {len(tokens)} tokens fetched!\n")
        pprint(tokens)
