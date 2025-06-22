# bot/alpha_sniffer.py  –  GeckoTerminal “new-pool” watcher (Solana)

import asyncio, requests
from datetime import datetime, timezone
from pathlib import Path
from loguru import logger

# ───────────────────────── CONFIG ──────────────────────────
NETWORK        = "solana"          # chain to watch
LOOKBACK_MIN   = 15                # pools younger than this many minutes
SCAN_INTERVAL  = 60                # seconds between API calls
DEBUG_LOG_ALL  = False             # True  ➜ log every pool’s age
LOG_FILE       = Path("data/new_tokens.txt")

# ── choose ONE endpoint ────────────────────────────────────
USE_SEARCH_API = False             # True = /search/pools, False = /networks/…/pools
if USE_SEARCH_API:
    API_URL = "https://api.geckoterminal.com/api/v2/search/pools"
    API_PARAMS = {"network": NETWORK, "sort": "recent", "page": 1}
else:
    API_URL = f"https://api.geckoterminal.com/api/v2/networks/{NETWORK}/pools"
    API_PARAMS = {"page": 1}
# ───────────────────────────────────────────────────────────

LOG_FILE.parent.mkdir(exist_ok=True)              # be sure data/ exists


def fetch_new_pools() -> list[tuple[str, str, datetime]]:
    """
    Return [(symbol, name, created_ts)] for pools created in
    the last LOOKBACK_MIN minutes (newest→oldest, page 1 only).
    """
    try:
        r = requests.get(API_URL, params=API_PARAMS, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])

        now   = datetime.now(timezone.utc)
        fresh = []

        for pool in data:
            attr        = pool.get("attributes", {})
            base_token  = attr.get("base_token", {})
            created_at  = attr.get("created_at")
            if not created_at:
                continue

            # GeckoTerminal timestamps are ISO-8601 with “Z”
            try:
                ts = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                continue

            age_min = (now - ts).total_seconds() / 60

            # —— diagnostic heartbeat ————————————————
            if DEBUG_LOG_ALL:
                logger.debug(
                    f"{base_token.get('symbol','?'):>8}  {age_min:5.1f} min old"
                )
            # ————————————————————————————————

            if age_min <= LOOKBACK_MIN:
                fresh.append(
                    (
                        base_token.get("symbol", "???"),
                        base_token.get("name",   "???"),
                        ts,
                    )
                )

        return fresh

    except Exception as exc:
        logger.error(f"❌  GeckoTerminal fetch error: {exc}")
        return []


async def fetch_and_log() -> None:
    fresh = fetch_new_pools()

    # Stay quiet unless we have news (or debug enabled)
    if not fresh:
        return

    logger.success(f"🆕  {len(fresh)} pool(s) ≤ {LOOKBACK_MIN} min")
    with LOG_FILE.open("a", encoding="utf-8") as fp:
        for symbol, name, ts in fresh:
            line = f"[NEW] {symbol} – {name}  ({ts.isoformat()} UTC)"
            logger.success(line)
            fp.write(line + "\n")


async def start_sniffer_loop() -> None:
    logger.info(
        f"🔎  Alpha-Sniffer started for {NETWORK} "
        f"(interval {SCAN_INTERVAL}s, look-back {LOOKBACK_MIN} min)…"
    )
    while True:
        await fetch_and_log()
        await asyncio.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    asyncio.run(start_sniffer_loop())
