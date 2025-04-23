from assistant.context import ContextManager
from assistant.commands import handle_command
from services.openai_service import ask_openai

ctx = ContextManager()

def main_loop():
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("NEXUS-X Core: Goodbye.")
            break

        if user_input.startswith("/"):
            result = handle_command(user_input)
        else:
            result = ask_openai(ctx.get_history(), user_input)
            ctx.add_message("user", user_input)
            ctx.add_message("assistant", result)

        print("NEXUS-X Core:", result)
