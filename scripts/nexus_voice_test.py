import pyaudio
import wave
import subprocess
import os

# Configuración general
RAW_FILE = "test_recording.wav"
CLEAN_FILE = "test_clean.wav"
SECONDS = 5
SAMPLE_RATE = 16000

def list_input_devices():
    print("\n🔍 Detectando dispositivos de entrada disponibles:")
    pa = pyaudio.PyAudio()
    devices = []
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            devices.append((i, info["name"]))
            print(f"[{i}] {info['name']} | Channels: {info['maxInputChannels']}")
    pa.terminate()
    return devices

def record_audio(device_index=None):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                     input=True, frames_per_buffer=1024,
                     input_device_index=device_index)

    print(f"\n🎙 Grabando {SECONDS} segundos...")
    frames = []
    for _ in range(0, int(SAMPLE_RATE / 1024 * SECONDS)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    wf = wave.open(RAW_FILE, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"✅ Grabación guardada en {RAW_FILE}")

def check_sox():
    if subprocess.call(['which', 'sox'], stdout=subprocess.DEVNULL) != 0:
        print("❗ [ERROR] sox no está instalado. Instálalo con: sudo apt install sox")
        return False
    return True

def resample_audio():
    if not os.path.exists(RAW_FILE):
        print(f"❗ [ERROR] No se encontró {RAW_FILE}")
        return False

    result = subprocess.run([
        "sox", RAW_FILE, "-c", "1", "-r", "48000", CLEAN_FILE
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"❗ [ERROR] Fallo en sox: {result.stderr.decode()}")
        return False

    print(f"✅ Archivo resampleado guardado en {CLEAN_FILE}")
    return True

if __name__ == "__main__":
    devices = list_input_devices()
    if not devices:
        print("❗ No se encontraron dispositivos de entrada.")
        exit(1)

    # Pregunta al usuario
    try:
        choice = int(input("\n👉 Ingresa el índice del dispositivo que quieres usar (o -1 para predeterminado): "))
    except ValueError:
        choice = -1

    device_index = None if choice == -1 else choice

    record_audio(device_index=device_index)

    if check_sox():
        if resample_audio():
            print("\n🔊 Puedes probar los archivos grabados con:")
            print(f"aplay {RAW_FILE}")
            print(f"aplay {CLEAN_FILE}")
