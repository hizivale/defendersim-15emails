import re
import json
import time
import requests

MAILPIT  = "http://127.0.0.1:8025"
DEFENDER = "http://127.0.0.1:9100"
TICKETS  = "http://127.0.0.1:9000"
OLLAMA   = "http://192.168.37.1:11434"
MODEL    = "mistral:7b-instruct"

SEEN = set()

def redact(text: str) -> str:
    if not text:
        return ""
    t = re.sub(r'https?://\S+', '[URL]', text)
    t = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', t)
    t = re.sub(r'\b\d{8,}\b', '[NUMBER]', t)
    return t[:1200]

def to_confidence(val) -> float:
    if isinstance(val, (int, float)):
        return max(0.0, min(1.0, float(val)))
    if isinstance(val, str):
        v = val.strip().lower()
        mapping = {"high": 0.85, "medium": 0.60, "low": 0.30}
        if v in mapping:
            return mapping[v]
        try:
            return max(0.0, min(1.0, float(v)))
        except Exception:
            return 0.50
    return 0.50

def list_messages():
    r = requests.get(f"{MAILPIT}/api/v1/messages", timeout=10)
    r.raise_for_status()
    return r.json().get("messages", [])

def get_message(mid: str):
    r = requests.get(f"{MAILPIT}/api/v1/message/{mid}", timeout=10)
    r.raise_for_status()
    return r.json()

def defender_scan(subject: str, sender: str, reply_to: str, body: str) -> dict:
    payload = {"subject": subject, "sender": sender, "reply_to": reply_to, "body": body}
    r = requests.post(f"{DEFENDER}/scan", json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def _extract_first_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise ValueError(f"LLM did not return JSON. First 200 chars: {text[:200]}")
    return json.loads(m.group(0))

def ollama_triage(def_out: dict, snippet: str) -> dict:
    prompt = (
        "Output ONLY one JSON object. No prose. No markdown.\n"
        "Keys:\n"
        "  category: phishing|bec|malware|spam|benign\n"
        "  severity: low|medium|high\n"
        "  confidence: number 0.0-1.0\n"
        "  score: integer 0-100\n"
        "  actions: array of allow|quarantine|block_sender|reset_password|user_awareness\n"
        "  reason: <= 18 words\n\n"
        f"Defender JSON:\n{json.dumps(def_out)}\n\n"
        f"Redacted snippet:\n{snippet}\n"
    )

    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=180
    )
    r.raise_for_status()
    out = r.json().get("response", "").strip()
    return _extract_first_json(out)

def final_score(def_score: int, llm_score: int) -> int:
    return int(round(def_score * 0.6 + llm_score * 0.4))

def create_ticket(mid, subject, sender, def_out, llm_out, final):
    payload = {
        "mailpit_id": mid,
        "subject": subject,
        "sender": sender,
        "defender_score": int(def_out.get("score", 0)),
        "defender_verdict": def_out.get("verdict", "unknown"),
        "llm_category": llm_out.get("category", "benign"),
        "llm_severity": llm_out.get("severity", "low"),
        "llm_confidence": to_confidence(llm_out.get("confidence", 0.5)),
        "final_score": int(final),
        "summary": llm_out.get("reason", "")
    }
    r = requests.post(f"{TICKETS}/tickets", json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    print("Importer running. Polling Mailpit...", flush=True)
    while True:
        for m in list_messages():
            mid = m.get("ID")
            if not mid or mid in SEEN:
                continue

            try:
                msg = get_message(mid)
                hdr = msg.get("Headers", {})
                subject = (hdr.get("Subject") or ["(no subject)"])[0]
                sender  = (hdr.get("From") or ["(unknown)"])[0]
                reply_to = (hdr.get("Reply-To") or [""])[0]
                body = msg.get("Text", "") or ""

                def_out = defender_scan(subject, sender, reply_to, body)
                llm_out = ollama_triage(def_out, redact(body))

                fs = final_score(
                    int(def_out.get("score", 0)),
                    int(llm_out.get("score", 50))
                )

                t = create_ticket(mid, subject, sender, def_out, llm_out, fs)
                print(f"Ticket {t['id']} created. Defender={def_out.get('score')} LLM={llm_out.get('score')} Final={fs}", flush=True)

            except Exception as e:
                print(f"Failed for {mid}: {e}", flush=True)

            SEEN.add(mid)

        time.sleep(5)

if __name__ == "__main__":
    main()
