# bot/commands.py

def parse_command(input_text: str):
    input_text = input_text.strip().lower()

    if "buy" in input_text:
        return "BUY"
    elif "sell" in input_text:
        return "SELL"
    elif "status" in input_text:
        return "STATUS"
    elif "rebalance" in input_text:
        return "REBALANCE"
    else:
        return "UNKNOWN"
 
