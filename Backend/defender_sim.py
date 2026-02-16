from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import re

app = FastAPI(title="DefenderSim", version="1.0")

class ScanRequest(BaseModel):
    subject: str = ""
    sender: str = ""
    reply_to: str = ""
    body: str = ""

def _has_url(text: str) -> bool:
    return bool(re.search(r"https?://", text, flags=re.I))

def _suspicious_url(text: str) -> bool:
    # simplistic: look for URL + keyword patterns
    return bool(re.search(r"https?://\S*(login|verify|password|reset|update|secure)\S*", text, flags=re.I))

def _display_name_mismatch(sender: str) -> bool:
    # placeholder heuristic: if it contains both angle bracket and unusual domain patterns
    return ("<" in sender and ">" in sender and not re.search(r"@company\.com", sender, flags=re.I))

def _keywords(text: str) -> List[str]:
    words = [
        ("urgent", 12),
        ("immediately", 10),
        ("password", 18),
        ("verify", 12),
        ("reset", 15),
        ("invoice", 12),
        ("wire", 20),
        ("gift card", 20),
        ("account", 10),
        ("suspended", 18),
    ]
    hits = []
    for w, _ in words:
        if w in text.lower():
            hits.append(w)
    return hits

def _score(req: ScanRequest) -> Dict:
    text = f"{req.subject}\n{req.body}\n{req.sender}\n{req.reply_to}".strip()
    score = 0
    reasons = []

    hits = _keywords(text)
    if hits:
        score += min(35, len(hits) * 8)
        reasons.append(f"keyword_hits={hits[:6]}")

    if _has_url(text):
        score += 15
        reasons.append("contains_url")

    if _suspicious_url(text):
        score += 25
        reasons.append("suspicious_url_pattern")

    if _display_name_mismatch(req.sender):
        score += 10
        reasons.append("sender_domain_mismatch")

    # clamp
    score = max(0, min(100, score))

    if score >= 75:
        verdict = "malicious"
        severity = "high"
        action = "quarantine"
    elif score >= 45:
        verdict = "suspicious"
        severity = "medium"
        action = "quarantine"
    else:
        verdict = "clean"
        severity = "low"
        action = "allow"

    signals = {
        "contains_url": _has_url(text),
        "suspicious_url_pattern": _suspicious_url(text),
        "keyword_hits": hits[:10],
        "sender_domain_mismatch": _display_name_mismatch(req.sender),
    }

    return {
        "verdict": verdict,
        "severity": severity,
        "recommended_action": action,
        "score": score,
        "reasons": reasons,
        "signals": signals,
    }

@app.post("/scan")
def scan(req: ScanRequest):
    return _score(req)
