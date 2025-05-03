# NEXUS-X Core

NEXUS-X Core is a local, voice-enabled AI assistant built to run on a Raspberry Pi (or Ubuntu) as the physical extension of the NEXUS-X Telegram bot. It uses GPT-4 for natural conversation and is designed with a modular architecture, making it easy to expand with voice commands, integrations, or new AI providers.

---

## 🌟 Features

- ✅ **GPT-powered chat** with contextual memory
- ✅ **Command system** (/time, /hello, /estado, /reiniciar, etc.)
- ✅ **Wake word activation** (via Picovoice Porcupine)
- ✅ **Voice input** (Whisper) and **voice output** (TTS)
- ✅ **Modular design** (easily plug in new services or commands)
- ✅ **Multi-language support** (default language: Spanish, but configurable)
- ✅ **Optimized for Raspberry Pi OS Lite** (64-bit), but works on Ubuntu/Linux x86_64 too

---

## 📦 Requirements

- **Python**: 3.11+
- **Installed tools**: `sox`, `aplay`
- **Python libraries**:
  - `openai`
  - `python-dotenv`
  - `pvporcupine`
  - `pyaudio`
  - `TTS`

---

## 🛠️ Setup

```bash
# Clone the project
git clone https://github.com/your-username/nexus-x-core.git
cd nexus-x-core

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (if missing)
sudo apt install sox alsa-utils portaudio19-dev

# Prepare the .env file
cp .env.example .env
```

Edit `.env` and add:
```env
OPENAI_API_KEY=your_openai_api_key
ACCESS_KEY_UBUNTU=your_porcupine_access_key (if on Ubuntu)
ACCESS_KEY_RPI=your_porcupine_access_key (if on Raspberry Pi)
KEYWORD_PATH_UBUNTU=path_to_your_wakeword.ppn
KEYWORD_PATH_RPI=path_to_your_wakeword.ppn
```

---

## 🚀 Run the Assistant

```bash
python scripts/run.py
```

---

## 💡 Example Commands

In text or voice, you can use:

- `/hello` → Greets you
- `/time` → Tells current time
- `/modo default` → Changes mode
- `/lang es` → Switches language
- `/recordar something` → Adds a reminder
- `/ver` → Lists reminders
- `/borrar 1` → Deletes reminder #1

---

## 🛡️ Notes

- For best performance, use the Whisper CLI compiled for your platform.
- The system uses a rotating set of sci-fi activation responses (inspired by Blade Runner) when the wake word is detected.

