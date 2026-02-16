# Backend Setup

## Requirements

- Python 3.11+
- Git
- Mailpit
- Ollama (llama3.2:3b)

---

## Python Installation

### Ubuntu / Linux

sudo apt update && sudo apt upgrade -y  
sudo apt install -y python3.11 python3.11-venv python3-pip  
sudo apt install -y build-essential git curl wget  

Verify:
python3.11 --version  

### macOS

brew install python@3.11  
python3.11 --version  

### Windows

1. Download Python 3.11 from https://www.python.org/downloads/
2. Enable “Add Python to PATH”
3. Verify: python --version

---

## Backend Installation

git clone https://github.com/hizivale/defendersim-backend.git  
cd defendersim-backend  

python3.11 -m venv venv  

Activate:

Linux/macOS:
source venv/bin/activate  

Windows:
venv\Scripts\activate  

pip install --upgrade pip  
pip install -r requirements.txt  

---

## Environment Configuration

cp .env.example .env  

Example configuration:

MAILPIT_API_URL=http://127.0.0.1:8025/api/v1  
OLLAMA_API_URL=http://127.0.0.1:11434/api/generate  
OLLAMA_MODEL=llama3.2:3b  
BACKEND_PORT=9100  
TICKET_API_PORT=9000  

ML_WEIGHT=0.3  
SIGNATURE_WEIGHT=0.4  
OLLAMA_WEIGHT=0.3  

LOG_LEVEL=INFO  

---

## Verification

Test Mailpit:
curl http://127.0.0.1:8025/api/v1/messages  

Test Ollama:
curl http://127.0.0.1:11434/api/tags  

Start backend:
python server.py  
