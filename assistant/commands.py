from datetime import datetime

def handle_command(command: str) -> str:
    if command == "/time":
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif command == "/hello":
        return "Hello! I'm NEXUS-X Core, your personal assistant."
    else:
        return "Unknown command. Try /time or /hello."
