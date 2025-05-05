import threading
import argparse

from assistant.core import main_loop
from gui import start_gui

def parse_args():
    parser = argparse.ArgumentParser(description="Start NEXUS-X Core assistant.")
    parser.add_argument("--mode", type=str, help="Conversational mode (default, programador, filosofico, etc.)")
    parser.add_argument("--lang", type=str, help="Language (es, en)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Lanza main_loop en segundo plano
    backend_thread = threading.Thread(target=main_loop, kwargs={"mode": args.mode, "lang": args.lang}, daemon=True)
    backend_thread.start()

    print(f"Lanzando interfaz gráfica...")
    # Kivy siempre en el hilo principal
    start_gui()
