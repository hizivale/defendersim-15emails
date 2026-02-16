# Development Workflow

## Start Environment

Terminal 1:
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog  

Terminal 2:
ollama serve  

Terminal 3:
source venv/bin/activate  
python server.py  

---

## Run Tests

python -m pytest tests/  

---

## Code Quality

pylint server.py  
black server.py  
mypy server.py  

---

## Seed Test Data

python import_and_triage.py  

Analyze all:
python defender_sim.py --analyze-all  
