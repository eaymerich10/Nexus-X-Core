
---

### 📄 `setup.sh`
```bash
#!/bin/bash

echo "🔧 Setting up NEXUS-X Core on your Raspberry Pi..."

# System update
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Clone the repo (change to your actual GitHub link)
git clone https://github.com/your-username/nexus-x-core.git
cd nexus-x-core

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Setup complete
echo "✅ NEXUS-X Core setup complete."
echo "🔑 Don't forget to add your OpenAI key to .env"
