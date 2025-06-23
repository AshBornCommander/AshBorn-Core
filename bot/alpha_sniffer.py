# bot/alpha_sniffer.py  –  AshBorn BirdEye “new-token” watcher (Solana)

import asyncio, requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from loguru import logger

# ───────────────────────── CONFIG ──────────────────────────
LOOKBACK_MIN   = 10                       # consider tokens ≤ N minutes old
SCAN_INTERVAL  = 60                       # seconds between API calls
LOG_FILE       = Path("data/new_tokens.txt")

# BirdEye public endpoint (no key needed for this route)
# Docs: https://docs.birdeye.so/reference/get_token_recently_updated
BIRDEYE_URL = "https://public-api.birdeye.so/public/token/updated"
HEADERS     = {"accept": "application/json", "x-chain": "solana"}
# ───────────────────────────────────────────────────────────

LOG_FILE.parent.mkdir(exist_ok=True)

seen_addresses: set[str] = set()          # dedup within this session


def fetch_new_tokens(minutes: int = LOOKBACK_MIN):
    """
    Return list of (symbol, name, addr, created_dt) for tokens
    whose metadata updated within the last <minutes> minutes.
    """
    try:
        # BirdEye expects a unix timestamp (seconds)
        cutoff_ts = int((datetime.utcnow() - timedelta(minutes=minutes)).timestamp())
        params = {"time": cutoff_ts}

        r = requests.get(BIRDEYE_URL, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        raw = r.json().get("data", [])

        fresh = []
        now   = datetime.now(timezone.utc)

        for item in raw:
            addr = item.get("address")
            if not addr or addr in seen_addresses:
                continue

            # BirdEye returns "updated_unix" (seconds) – use as created time
            created_ts = item.get("updated_unix") or item.get("created_unix")
            if not created_ts:
                continue
            created_dt = datetime.fromtimestamp(created_ts, timezone.utc)
            age_min = (now - created_dt).total_seconds() / 60

            if age_min <= minutes:
                fresh.append((
                    item.get("symbol", "???"),
                    item.get("name",   "???"),
                    addr,
                    created_dt,
                ))
                seen_addresses.add(addr)

        logger.success(f"✅  {len(fresh)} new token(s) ≤ {minutes} min")
        return fresh

    except Exception as exc:
        logger.error(f"❌ BirdEye fetch error: {exc}")
        return []


async def fetch_and_log():
    tokens = fetch_new_tokens()
    if not tokens:
        return

    with LOG_FILE.open("a", encoding="utf-8") as fp:
        for sym, name, addr, ts in tokens:
            line = f"[NEW] {sym} – {name} | {addr}  ({ts.isoformat()} UTC)"
            logger.info(line)
            fp.write(line + "\n")


async def start_sniffer_loop():
    logger.info(
        f"🔎 BirdEye Alpha-Sniffer started "
        f"(interval {SCAN_INTERVAL}s | look-back {LOOKBACK_MIN} min)"
    )
    while True:
        await fetch_and_log()
        await asyncio.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    asyncio.run(start_sniffer_loop())
