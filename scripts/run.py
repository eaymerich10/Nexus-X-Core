from assistant.core import main_loop
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Start NEXUS-X Core assistant.")
    parser.add_argument("--mode", type=str, help="Conversational mode (default, programador, filosofico, etc.)")
    parser.add_argument("--lang", type=str, help="Language (es, en)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(f"🔊 NEXUS-X Core initialized. Starting main loop...")
    main_loop(mode=args.mode, lang=args.lang)
