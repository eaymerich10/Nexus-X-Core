import pyaudio

pa = pyaudio.PyAudio()
print("\n🎤 INPUT / OUTPUT AUDIO DEVICES:\n")

for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    name = info['name']
    max_input = info['maxInputChannels']
    max_output = info['maxOutputChannels']
    print(f"[{i}] {name} | Input Channels: {max_input} | Output Channels: {max_output}")

pa.terminate()
