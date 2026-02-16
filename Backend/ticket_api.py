from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Ticket API", version="1.0")

DB_PATH = "tickets.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        mailpit_id TEXT,
        subject TEXT,
        sender TEXT,
        defender_score INTEGER,
        defender_verdict TEXT,
        llm_category TEXT,
        llm_severity TEXT,
        llm_confidence REAL,
        final_score INTEGER,
        summary TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

class TicketCreate(BaseModel):
    mailpit_id: str
    subject: str
    sender: str
    defender_score: int = 0
    defender_verdict: str = "unknown"
    llm_category: str = "benign"
    llm_severity: str = "low"
    llm_confidence: float = 0.5
    final_score: int = 0
    summary: str = ""

class TicketOut(TicketCreate):
    id: int
    created_at: str

@app.get("/tickets", response_model=List[TicketOut])
def list_tickets():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, created_at, mailpit_id, subject, sender, defender_score, defender_verdict, llm_category, llm_severity, llm_confidence, final_score, summary FROM tickets ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    out = []
    for r in rows:
        out.append({
            "id": r[0],
            "created_at": r[1],
            "mailpit_id": r[2],
            "subject": r[3],
            "sender": r[4],
            "defender_score": r[5],
            "defender_verdict": r[6],
            "llm_category": r[7],
            "llm_severity": r[8],
            "llm_confidence": float(r[9]),
            "final_score": r[10],
            "summary": r[11],
        })
    return out

@app.post("/tickets", response_model=TicketOut)
def create_ticket(t: TicketCreate):
    created_at = datetime.utcnow().isoformat() + "Z"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tickets (created_at, mailpit_id, subject, sender, defender_score, defender_verdict, llm_category, llm_severity, llm_confidence, final_score, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        created_at, t.mailpit_id, t.subject, t.sender, t.defender_score, t.defender_verdict,
        t.llm_category, t.llm_severity, float(t.llm_confidence), t.final_score, t.summary
    ))
    conn.commit()
    tid = cur.lastrowid
    conn.close()

    return {
        "id": tid,
        "created_at": created_at,
        **t.model_dump()
    }
