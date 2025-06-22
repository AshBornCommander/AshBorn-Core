# sniffers/alpha_sniffer.py

import time
import random

seen_addresses = set()

def simulate_fresh_listings():
    mock_tokens = [
        {"name": "PEPEKING", "address": "So1P3p3KingFakeA1phaToken"},
        {"name": "RUGFREE", "address": "So1RugFreeAlphaExample"},
        {"name": "BURNX100", "address": "So1BurnFastFakeListing"},
    ]
    while True:
        token = random.choice(mock_tokens)
        if token["address"] not in seen_addresses:
            print(f"[ALPHA] New Token Detected: {token['name']} ({token['address']})")
            seen_addresses.add(token["address"])
        time.sleep(5)

if __name__ == "__main__":
    simulate_fresh_listings()

