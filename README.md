# 🤖 AshBorn Core

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://python.org)
[![Solana](https://img.shields.io/badge/Solana-Mainnet-9945FF?logo=solana&logoColor=white)](https://solana.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

**An autonomous Solana trading intelligence system — sniff alpha, execute trades, and control everything through Telegram.**

</div>

---

## 📖 Overview

**AshBorn Core** is a fully autonomous, multi-threaded Python trading bot built for the Solana ecosystem. It continuously sniffs for emerging token opportunities, evaluates alpha signals through an intelligent brain loop, and executes trades — all while being remotely controllable via a Telegram interface or a local command file. Designed for low-latency, always-on operation with clean separation of concerns across its bot, sniffer, and utility layers.

---

## ✨ Features

### 🔎 Alpha Sniffer
- Continuously monitors the Solana network for new and trending token activity
- Runs on a dedicated async event loop for non-blocking, real-time performance
- Configurable scan intervals and token filters

### 🧠 Brain (Intelligence Layer)
- Background task scheduler that evaluates alpha signals from the sniffer
- Applies configurable logic to determine buy/sell/hold decisions
- Runs co-located on the same async loop as the sniffer for tight integration

### 📲 Telegram Remote Control
- Full bot interface via `python-telegram-bot` for remote command execution
- Issue trade commands, query status, and monitor activity from anywhere
- Runs in its own daemon thread — always listening, never blocking

### 📄 Local Command File Watcher
- Monitors `command.txt` in real time for direct trade instructions
- Simple human-readable format: e.g., `BUY USDC 0.2`
- Useful for local testing, scripting, or fallback control
- Runs as the main thread's blocking loop

### 🗂️ Structured Logging
- Powered by `loguru` with configurable log levels via `.env`
- Colour-coded console output via `colorama`
- Log files stored under the `logs/` directory

### 🧪 Testnet Support
- Dedicated `testnet/` directory for safe strategy testing before going live
- Swap between mainnet and testnet via environment config

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11+ |
| Async Runtime | `asyncio` + `threading` |
| Telegram Interface | `python-telegram-bot` 20.7 |
| HTTP Client | `httpx` 0.25 + `requests` 2.32 |
| Scheduling | `APScheduler` 3.6 |
| Logging | `loguru` 0.7 |
| Configuration | `python-dotenv` |
| Console Output | `colorama` |

---

## 📂 Project Structure

```
AshBorn-Core/
├── main.py                    # Boot sequence — wires all threads together
├── command.txt                # Local trade command interface (e.g. BUY USDC 0.2)
├── requirements.txt           # Python dependencies
├── .env                       # Environment config (API keys, bot token, log level)
│
├── bot/
│   ├── brain.py               # 🧠 Alpha evaluation & background task scheduler
│   ├── telegram_bot.py        # 📲 Telegram polling bot
│   └── realtime.py            # 👁️ command.txt file watcher
│
├── sniffers/
│   └── alpha_sniffer.py       # 🔎 Solana token discovery loop
│
├── config/                    # Configuration files and constants
├── data/                      # Persistent trade/signal data
├── wallets/                   # Wallet management utilities
├── utils/                     # Shared helper functions
├── scripts/                   # Standalone utility scripts
├── testnet/                   # Testnet environment for safe testing
├── logs/                      # Runtime log files
└── archives/                  # Historical trade archives
```

---

## ⚙️ Architecture

AshBorn Core runs three concurrent execution paths from a single `main()` boot sequence:

```
main()
 ├── Thread 1 — TelegramThread   → python-telegram-bot polling (daemon)
 ├── Thread 2 — SnifferThread    → asyncio event loop (daemon)
 │    ├── Brain background tasks  (launch_background_tasks)
 │    └── Alpha sniffer loop      (start_sniffer_loop)
 └── Main Thread                 → command.txt watcher (blocking loop)
```

The sniffer and brain intentionally share the same `asyncio` event loop — this keeps token signal evaluation tightly coupled with discovery without the overhead of inter-thread queues.

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.11+
A Solana wallet with funded keypair
A Telegram Bot token (via @BotFather)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/AshBornCommander/AshBorn-Core.git
cd AshBorn-Core

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
BOT_NAME=AshBorn
LOG_LEVEL=INFO
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
WALLET_PRIVATE_KEY=your_wallet_private_key
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

### Run

```bash
python main.py
```

You'll see the boot banner:

```
🤖 [AshBorn] is waking up at 2026-04-13T09:00:00 …
```

---

## 💬 Command Reference

### Telegram Commands

| Command | Description |
|---|---|
| `/status` | Check bot health and active threads |
| `/buy <token> <amount>` | Execute a buy order |
| `/sell <token> <amount>` | Execute a sell order |
| `/sniff` | Manually trigger alpha scan |
| `/log` | View recent activity log |

### Local Command File (`command.txt`)

Write a trade command directly into `command.txt` and the watcher will execute it:

```
BUY USDC 0.2
```

```
SELL SOL 1.5
```

---

## 🔒 Security Notes

- Wallet private keys are loaded exclusively from environment variables — never hardcoded
- The `.gitignore` excludes all `.env` files, wallet files, and log outputs
- The `wallets/` directory is not committed to version control
- Testnet mode is recommended for all strategy development and testing

---

## 🗺️ Roadmap

- [ ] Multi-wallet support
- [ ] Webhook-based Telegram interface (replace polling)
- [ ] On-chain position tracking dashboard
- [ ] Strategy plugin architecture
- [ ] Docker containerisation for cloud deployment
- [ ] Automated stop-loss / take-profit logic

---

## 👨‍💻 Developer

**Pavan Kumar Malladi**
Data Engineer & Systems Developer
Phoenix, Arizona

- GitHub: [@AshBornCommander](https://github.com/AshBornCommander)
- Email: [pavankumarmalladi7@gmail.com](mailto:pavankumarmalladi7@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.

---

> *Built for speed, autonomy, and precision — AshBorn never sleeps.* ⚡
