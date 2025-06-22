import time
from pathlib import Path
from .commands import parse_command
from .brain import handle_command

COMMAND_FILE = Path("command.txt")
LAST_COMMAND = ""

def watch_command_file():
    global LAST_COMMAND
    print("🟢 AshBorn is listening for new commands in 'command.txt'...\n")
    
    while True:
        if not COMMAND_FILE.exists():
            time.sleep(1)
            continue
        
        with COMMAND_FILE.open("r") as f:
            command = f.read().strip()
        
        if command and command != LAST_COMMAND:
            print(f"\n📥 New Command Detected: {command}")
            parsed = parse_command(command)
            if parsed:
                handle_command(parsed)
            else:
                print("⚠️ Invalid command format.")
            LAST_COMMAND = command
        
        time.sleep(2)
 
