# DefenderSim Backend Setup Guide

## Quick Start (10 Minutes)

### Prerequisites

Ensure you have installed:
- Python 3.11 or later
- Ollama with Llama 3.2:3b model
- Mailpit SMTP server
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/hizivale/defendersim-backend.git
cd defendersim-backend
```

### Step 2: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```
MAILPIT_API_URL=http://127.0.0.1:8025/api/v1
OLLAMA_API_URL=http://127.0.0.1:11434/api/generate
OLLAMA_MODEL=llama3.2:3b
BACKEND_PORT=9100
TICKET_API_PORT=9000
```

### Step 5: Start Services

In separate terminals:

```bash
# Terminal 1: Mailpit
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Terminal 2: Ollama
ollama serve

# Terminal 3: Backend
source venv/bin/activate
python server.py
```

Backend available at http://localhost:9100

---

## Detailed Installation Guide

### 1. Python Installation

#### Ubuntu/Linux

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install build tools
sudo apt install -y build-essential git curl wget

# Verify installation
python3.11 --version
pip3 --version
```

#### macOS

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3.11 --version
pip3 --version
```

#### Windows

1. Download Python 3.11 from https://www.python.org/downloads/
2. Run installer
3. Check "Add Python to PATH"
4. Click "Install Now"
5. Verify in PowerShell: `python --version`

### 2. Mailpit Installation

#### Option A: Docker (Recommended)

```bash
# Install Docker
# Ubuntu: sudo apt install docker.io
# macOS: brew install docker
# Windows: Download Docker Desktop

# Run Mailpit
docker run -d \
  -p 1025:1025 \
  -p 8025:8025 \
  --name mailpit \
  mailhog/mailhog

# Access web interface
# http://localhost:8025
```

#### Option B: Binary Installation

1. Download from https://mailpit.axllent.org/
2. Extract binary
3. Run: `./mailpit`
4. Access at http://localhost:8025

#### Option C: Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mailpit:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    environment:
      MH_HOSTNAME: mailpit
      MH_STORAGE: memory
```

Run:
```bash
docker-compose up -d
```

### 3. Ollama Installation

#### Installation

1. Download from https://ollama.ai
2. Install for your operating system
3. Run installer

#### Pull Model

```bash
ollama pull llama3.2:3b
```

Wait for model download (2-3 GB)

#### Start Server

```bash
ollama serve
```

Ollama will start on http://localhost:11434

#### Verify Installation

```bash
curl http://localhost:11434/api/tags
```

Should return list of available models including `llama3.2:3b`

### 4. Backend Installation

#### Clone Repository

```bash
git clone https://github.com/hizivale/defendersim-backend.git
cd defendersim-backend
```

#### Create Virtual Environment

```bash
# Create venv
python3.11 -m venv venv

# Activate venv
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

Your terminal prompt should show `(venv)` indicating venv is active.

#### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Create Environment File

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```
# Mailpit Configuration
MAILPIT_API_URL=http://127.0.0.1:8025/api/v1

# Ollama Configuration
OLLAMA_API_URL=http://127.0.0.1:11434/api/generate
OLLAMA_MODEL=llama3.2:3b

# Server Configuration
BACKEND_PORT=9100
TICKET_API_PORT=9000

# Analysis Configuration
ML_WEIGHT=0.3
SIGNATURE_WEIGHT=0.4
OLLAMA_WEIGHT=0.3

# Logging
LOG_LEVEL=INFO
```

#### Verify Configuration

Test connections:

```bash
# Test Mailpit
curl http://127.0.0.1:8025/api/v1/messages

# Test Ollama
curl http://127.0.0.1:11434/api/tags

# Start backend
python server.py
```

Expected output:
```
Initializing detection systems...
ML model loaded successfully
RAG system initialized: X examples
Uvicorn running on http://127.0.0.1:9100
```

---

## VMware Setup (For Mac Users)

### Prerequisites

- Mac with Intel or Apple Silicon processor
- 16 GB RAM minimum (32 GB recommended)
- 50 GB free disk space
- Stable internet connection

### Step 1: Install VMware Fusion

1. Visit https://www.vmware.com/products/fusion/fusion-evaluation.html
2. Download VMware Fusion Player (free for personal use)
3. Create VMware account and get license key
4. Install on Mac
5. Grant system permissions (Accessibility, Network Extensions)

### Step 2: Create Ubuntu VM

1. Download Ubuntu Server 22.04 LTS ISO
2. Open VMware Fusion and click "Create a New Virtual Machine"
3. Select "Install from disc or image"
4. Choose Ubuntu ISO
5. Configure VM:
   - Processors: 4-8 cores
   - Memory: 8-16 GB
   - Disk: 50-100 GB
   - Network: Bridged Networking
6. Start VM and complete Ubuntu installation
7. Note the assigned IP address (e.g., 192.168.37.128)

### Step 3: Setup Backend in VM

SSH into VM:
```bash
ssh username@192.168.37.128
```

Follow "Detailed Installation Guide" above starting from Python Installation.

### Step 4: Access from Mac

Backend is accessible from Mac at:
```
http://192.168.37.128:9100
```

Or use ngrok for public access:
```bash
# Install ngrok
brew install ngrok

# Expose backend
ngrok http 9100

# Share public URL
```

---

## Service Startup Sequence

### Development Environment

Start services in this order:

1. **Mailpit** (email ingestion):
```bash
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

2. **Ollama** (LLM server):
```bash
ollama serve
```

3. **Backend** (API server):
```bash
cd defendersim-backend
source venv/bin/activate
python server.py
```

### Production Environment

Use process manager (systemd) for automatic restarts:

Create `/etc/systemd/system/defendersim-backend.service`:
```ini
[Unit]
Description=DefenderSim Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/defendersim-backend
ExecStart=/home/ubuntu/defendersim-backend/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable defendersim-backend
sudo systemctl start defendersim-backend
sudo systemctl status defendersim-backend
```

---

## Testing Services

### Test Mailpit Connection

```bash
curl http://127.0.0.1:8025/api/v1/messages
```

Expected response: JSON array of messages

### Test Ollama Connection

```bash
curl http://127.0.0.1:11434/api/tags
```

Expected response: JSON with available models

### Test Backend Health

```bash
curl http://127.0.0.1:9100/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "backend": "running",
  "mailpit": "connected",
  "ollama": "running"
}
```

### Test Email Analysis

```bash
curl http://127.0.0.1:9100/api/emails
```

Expected response: JSON array of emails with analysis

---

## Seeding Test Data

### Load Sample Emails

```bash
python import_and_triage.py
```

This will:
1. Load 15 sample phishing emails
2. Import into Mailpit
3. Analyze each email
4. Store results locally

Expected output:
```
Loading 15 sample emails...
Email 1: Deutsche Bank phishing (German)
Email 2: PayPal phishing (English)
...
Email 15: Telekom billing (German)
Import complete: 15 emails loaded
```

### Analyze All Emails

```bash
python defender_sim.py --analyze-all
```

This will:
1. Retrieve all emails from Mailpit
2. Run analysis for each email
3. Store results locally
4. Generate statistics

---

## Troubleshooting

### Python Version Mismatch

**Error:** `python3.11: command not found`

**Solutions:**
1. Check installed versions: `python3 --version`
2. Use available version: `python3 -m venv venv`
3. Or install Python 3.11 explicitly

### Virtual Environment Not Activating

**Error:** `(venv) prompt not showing`

**Solutions:**
1. Verify venv exists: `ls venv/`
2. Re-create venv: `rm -rf venv && python3 -m venv venv`
3. Activate again: `source venv/bin/activate`

### Mailpit Connection Failed

**Error:** `Error: connect ECONNREFUSED 127.0.0.1:1025`

**Solutions:**
1. Verify Mailpit running: `docker ps | grep mailpit`
2. Check port: `lsof -i :1025`
3. Restart Mailpit: `docker restart mailpit`

### Ollama Connection Failed

**Error:** `Error: Failed to connect to Ollama`

**Solutions:**
1. Verify Ollama running: `ollama list`
2. Check port: `lsof -i :11434`
3. Verify model: `ollama pull llama3.2:3b`
4. Restart Ollama: `pkill ollama && ollama serve`

### Port Already in Use

**Error:** `Address already in use`

**Solutions:**
1. Find process: `lsof -i :9100`
2. Kill process: `kill -9 <PID>`
3. Or use different port in `.env`: `BACKEND_PORT=9101`

### ML Model Not Found

**Error:** `FileNotFoundError: phishing_model.pkl`

**Solutions:**
1. Train model: `python train_model.py`
2. Or download pre-trained: `wget https://...`
3. Verify files: `ls *.pkl`

### Dependencies Installation Failed

**Error:** `pip install -r requirements.txt` fails

**Solutions:**
1. Update pip: `pip install --upgrade pip`
2. Install build tools: `sudo apt install build-essential`
3. Install individually: `pip install fastapi uvicorn`
4. Check Python version: `python --version`

---

## Development Workflow

### Start Development Environment

```bash
# Terminal 1: Mailpit
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Terminal 2: Ollama
ollama serve

# Terminal 3: Backend
cd defendersim-backend
source venv/bin/activate
python server.py
```

### Make Code Changes

1. Edit Python files in `defendersim-backend/`
2. Backend automatically restarts (with auto-reload)
3. Test changes via API or frontend

### Run Tests

```bash
python -m pytest tests/
```

### Check Code Quality

```bash
pylint server.py
black server.py
mypy server.py
```

---

## Production Deployment

### Prepare for Production

1. Update `.env` for production:
```
BACKEND_PORT=8000
LOG_LEVEL=WARNING
```

2. Build application:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest tests/
```

### Deploy to Linux Server

1. SSH into server
2. Clone repository
3. Create virtual environment
4. Install dependencies
5. Configure `.env`
6. Start with systemd

### Deploy with Docker

```bash
# Build image
docker build -t defendersim-backend .

# Run container
docker run -p 9100:9100 \
  -e MAILPIT_API_URL="http://mailpit:8025/api/v1" \
  -e OLLAMA_API_URL="http://ollama:11434/api/generate" \
  defendersim-backend
```

### Deploy with Docker Compose

```bash
docker-compose up -d
```

---

## Monitoring and Maintenance

### Check Service Status

```bash
# Backend
curl http://localhost:9100/api/health

# Mailpit
curl http://localhost:8025/api/v1/messages

# Ollama
curl http://localhost:11434/api/tags
```

### View Logs

```bash
# Backend logs
tail -f logs/backend.log

# System logs (if using systemd)
journalctl -u defendersim-backend -f
```

### Restart Services

```bash
# Restart backend
pkill -f "python server.py"
python server.py

# Or with systemd
sudo systemctl restart defendersim-backend
```

### Performance Monitoring

```bash
# Check system resources
top

# Check disk usage
df -h

# Check memory usage
free -h
```

---

## Support and Resources

### Documentation

- README.md: Project overview
- ARCHITECTURE.md: System design
- API_DOCUMENTATION.md: API endpoints

### External Resources

- Python: https://www.python.org
- FastAPI: https://fastapi.tiangolo.com
- Mailpit: https://mailpit.axllent.org
- Ollama: https://ollama.ai
- VMware Fusion: https://www.vmware.com/products/fusion

### Getting Help

1. Check logs for error messages
2. Review troubleshooting section
3. Open issue on GitHub
4. Contact project maintainer

---

**Version:** 1.0  
**Last Updated:** February 2026
