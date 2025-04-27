import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.speech.speech_service import SpeechService

def procesar_entrada_usuario(texto_usuario):
    """
    Función simulada para procesar lo que dice el usuario.
    Aquí en el futuro conectaríamos con OpenAI o el cerebro real de NEXUS.
    """
    if not texto_usuario:
        return "No he entendido lo que dijiste."
    return f"Tú dijiste: {texto_usuario}"

def main():
    # Inicializar el servicio de captura de voz
    speech_service = SpeechService(
        whisper_path="/home/enric/Proyectos/whisper.cpp/whisper-cli",
        model_path="/home/enric/Proyectos/whisper.cpp/models/ggml-tiny.bin"
    )

    print("🧠🎙️ NEXUS-X Core en modo escucha. Pulsa [ENTER] para hablar. Escribe 'q' para salir.\n")

    try:
        while True:
            comando = input("👉 [ENTER] para grabar ('q' para salir): ").strip().lower()
            if comando == "q":
                print("👋 Cerrando NEXUS-X Core...")
                break

            print("🎤 Grabando...")
            texto_usuario = speech_service.listen_and_transcribe()

            if texto_usuario:
                print(f"📝 Transcripción: {texto_usuario}\n")
                respuesta = procesar_entrada_usuario(texto_usuario)
                print(f"🤖 NEXUS-X responde: {respuesta}\n")
            else:
                print("❓ No se detectó voz o hubo un problema en la transcripción.\n")

    except KeyboardInterrupt:
        print("\n👋 Interrupción manual detectada. Cerrando NEXUS-X Core...")

if __name__ == "__main__":
    main()
