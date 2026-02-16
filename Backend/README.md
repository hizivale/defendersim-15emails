# DefenderSim Backend

DefenderSim is a phishing detection and email analysis backend integrating:
- FastAPI
- Machine learning classification
- Signature-based detection
- Ollama (LLM-based analysis)
- Mailpit (SMTP testing)

## Tech Stack

- Python 3.11+
- FastAPI
- Ollama (llama3.2:3b)
- Mailpit
- Docker (optional)

## Quick Start

### 1. Clone Repository

git clone https://github.com/hizivale/defendersim-backend.git  
cd defendersim-backend

### 2. Create Virtual Environment

python3.11 -m venv venv  
source venv/bin/activate  
pip install --upgrade pip  

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment

cp .env.example .env  

Edit `.env` as needed.

### 5. Start Services

Terminal 1:
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog  

Terminal 2:
ollama serve  

Terminal 3:
source venv/bin/activate  
python server.py  

Backend runs at:  
http://localhost:9100

## Documentation

Detailed documentation is available in the `docs/` directory:

- docs/setup.md
- docs/mailpit.md
- docs/ollama.md
- docs/development.md
- docs/deployment.md
- docs/troubleshooting.md
- docs/vmware.md
