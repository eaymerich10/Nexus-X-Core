# NEXUS-X Core

**NEXUS-X Core** is a local, voice-enabled AI assistant designed to run on a **Raspberry Pi** (or any Linux system like Ubuntu).  
It serves as the physical extension of the NEXUS-X Telegram bot, powered by **GPT-4** for natural conversations.  
The assistant is built with a modular architecture, making it easy to extend with new commands, services, or AI providers.

---

## 🌟 Features

- ✅ **Graphical interface built with Kivy** for touch or screen-based control (Raspberry Pi friendly)

- ✅ **GPT-4 powered chat** with contextual memory  
- ✅ **Voice and text commands** (`/time`, `/hello`, `/estado`, `/reiniciar`, etc.)  
- ✅ **Wake word activation** (via Picovoice Porcupine)  
- ✅ **Voice input** (Whisper CLI) and **voice output** (TTS: Coqui, Google, etc.)  
- ✅ **Modular architecture** – plug in new services easily  
- ✅ **Multi-language support** (default: Spanish, configurable)  
- ✅ **Optimized for Raspberry Pi OS Lite (64-bit)** — also runs on Ubuntu x86_64  

---

## 📦 Requirements

- **Python**: 3.11+  
- **System packages**:
  - `sox`, `aplay`, `alsa-utils`, `portaudio19-dev`
- **Python libraries**:
  - `openai`, `python-dotenv`, `pvporcupine`, `pyaudio`, `TTS`

---

## 🛠️ Setup

```bash
# Clone the project
git clone https://github.com/your-username/nexus-x-core.git
cd nexus-x-core

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies
sudo apt install sox alsa-utils portaudio19-dev

# Copy the environment configuration template
cp .env.example .env
```

Edit `.env` and fill in the following variables:

```env
OPENAI_API_KEY=your_openai_api_key

# Picovoice Porcupine credentials
ACCESS_KEY_UBUNTU=your_porcupine_access_key
ACCESS_KEY_RPI=your_porcupine_access_key

# Wake word paths
KEYWORD_PATH_UBUNTU=path_to_wakeword.ppn
KEYWORD_PATH_RPI=path_to_wakeword.ppn
```

---

## 🚀 Running the Assistant

```bash
python -m scripts.run
```

Once running, the assistant will listen for the wake word, process speech, and respond aloud.
---

## 🖥️ Graphical Interface

NEXUS-X Core includes a full graphical interface built with **Kivy**, optimized for touchscreens and embedded displays. It allows users to interact with the assistant in a more intuitive way, including:
- Input field and conversation history
- Visual feedback of processing and output
- Simple layout adapted to Raspberry Pi or Ubuntu

To launch the assistant with GUI support:

```bash
python -m scripts.run
```


## 📁 Project Structure

```bash
nexus-x-core/
├── assistant/            # Core assistant logic and context
│   ├── commands/         # Command handlers
│   ├── utils/            # Helpers and configuration
├── services/             # External services (TTS, memory, Supabase, etc.)
├── scripts/              # Runner scripts
├── .env.example          # Environment config template
├── install.sh            # Install as systemd user service
├── setup.sh              # One-time installation script
└── README.md
```

---

## 🛡️ Notes

- For best performance, compile and use the [Whisper CLI](https://github.com/ggerganov/whisper.cpp) appropriate for your platform.  
- Activation responses use a rotating set of sci-fi phrases inspired by *Blade Runner*.  
- All user interaction is designed to be modular and easily extendable.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 🤝 Contributions

Want to improve NEXUS-X Core? See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines. Feedback, issues and pull requests are welcome!


---

## 🔧 Setup scripts (optional)

This project includes two helper scripts for convenience:

### `setup.sh` – First-time setup
Use this to prepare your Raspberry Pi or Ubuntu environment (installs Python, dependencies, etc.)

```bash
chmod +x setup.sh
./setup.sh
```

### `install.sh` – Register as systemd user service
This will install NEXUS-X Core as a background service that auto-starts on boot (user-level, not root).

```bash
chmod +x install.sh
./install.sh

# Check status and logs
systemctl --user status nexus-x-core
journalctl --user -u nexus-x-core -f
```

To uninstall the service and clean up:

```bash
./uninstall.sh
```