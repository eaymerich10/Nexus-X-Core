# NEXUS-X Core

**NEXUS-X Core** is a local voice-enabled AI assistant built on a Raspberry Pi, designed to serve as the physical extension of the NEXUS-X Telegram bot. It uses GPT-4 for natural conversation and is modular for adding voice, commands, and integrations.

## 🌟 Features

- GPT-powered chat with contextual memory
- Command system (e.g. `/time`, `/hello`)
- Modular architecture (voice, search, Telegram bridge, etc.)
- Designed to run on Raspberry Pi OS Lite (64-bit)
- Multi-language support (default is language-agnostic)

## 📦 Requirements

- Python 3.11+
- `openai`, `python-dotenv`

## 🛠️ Setup

```bash
# Clone the project
git clone https://github.com/your-username/nexus-x-core.git
cd nexus-x-core

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenAI key to .env

# Run the assistant
python scripts/run.p
