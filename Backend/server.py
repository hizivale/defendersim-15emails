"""
Multi-Layer Phishing Detection Backend
Integrates: ML Classification + OWASP/CVE Signatures + RAG-Enhanced Ollama
"""
import os
import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pickle
import re

# Import detection modules
from signature_detector import SignatureDetector
from rag_system import RAGSystem

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MAILPIT_API_URL = os.getenv("MAILPIT_API_URL", "http://127.0.0.1:8025/api/v1")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# Initialize detection systems
print("🔧 Initializing detection systems...")
signature_detector = SignatureDetector()
rag_system = RAGSystem()

# Load ML model
ml_model = None
ml_vectorizer = None
try:
    with open('phishing_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        ml_vectorizer = pickle.load(f)
    print("✅ ML model loaded successfully")
except FileNotFoundError:
    print("⚠️  ML model not found. Run train_model.py first.")

# Get RAG statistics
rag_stats = rag_system.get_statistics()
print(f"✅ RAG system initialized: {rag_stats['total_examples']} examples")

class MLResult(BaseModel):
    prediction: str
    confidence: float
    top_features: List[str]

class SignatureResult(BaseModel):
    matched_patterns: List[str]
    matched_cves: List[str]
    malicious_domains: List[str]
    confidence: float

class OllamaResult(BaseModel):
    summary: str
    indicators: List[str]
    confidence: float
    riskLevel: str
    similar_examples: List[Dict]

class AnalysisResult(BaseModel):
    summary: str
    indicators: List[str]
    confidence: float
    riskLevel: str
    ml_analysis: Optional[MLResult] = None
    signature_analysis: Optional[SignatureResult] = None
    ollama_analysis: Optional[OllamaResult] = None

class Email(BaseModel):
    ID: str
    MessageID: str
    Read: bool
    From: Dict[str, Any]
    To: List[Dict[str, Any]]
    Subject: str
    Created: str
    Snippet: str
    Size: int
    Attachments: int
    Tags: List[str]
    analysis: Optional[AnalysisResult] = None

# In-memory storage for analysis results
analysis_cache = {}

def extract_ml_features(email_text: str, subject: str, sender: str) -> Dict[str, float]:
    """Extract features for ML model"""
    features = {}
    
    # Text features
    features['subject_length'] = len(subject)
    features['body_length'] = len(email_text)
    features['exclamation_marks'] = email_text.count('!')
    features['question_marks'] = email_text.count('?')
    features['capital_ratio'] = sum(1 for c in email_text if c.isupper()) / (len(email_text) + 1)
    
    # Urgency keywords
    urgency_words = ['urgent', 'immediate', 'act now', 'expires', 'limited time', 'hurry']
    features['urgency_keywords'] = sum(1 for word in urgency_words if word.lower() in email_text.lower())
    
    # Suspicious patterns
    features['contains_link'] = 1 if 'http' in email_text else 0
    features['contains_attachment'] = 0  # Would need actual attachment check
    features['typosquatting'] = 1 if any(domain in sender.lower() for domain in ['gmai1', 'yahooo', 'hotmial']) else 0
    features['requests_personal_info'] = 1 if any(word in email_text.lower() for word in ['password', 'ssn', 'credit card', 'bank account']) else 0
    
    return features

def analyze_with_ml(email_text: str, subject: str, sender: str) -> MLResult:
    """Analyze email with ML model"""
    if ml_model is None or ml_vectorizer is None:
        return MLResult(
            prediction="UNKNOWN",
            confidence=0.0,
            top_features=["ML model not available"]
        )
    
    try:
        # Extract features
        features = extract_ml_features(email_text, subject, sender)
        
        # Create feature vector
        feature_vector = ml_vectorizer.transform([email_text])
        
        # Predict
        prediction = ml_model.predict(feature_vector)[0]
        confidence = max(ml_model.predict_proba(feature_vector)[0])
        
        # Get top features
        top_features = []
        for key, value in sorted(features.items(), key=lambda x: abs(x[1]), reverse=True)[:3]:
            if value > 0:
                top_features.append(f"{key}: {value}")
        
        return MLResult(
            prediction="PHISHING" if prediction == 1 else "LEGITIMATE",
            confidence=float(confidence),
            top_features=top_features if top_features else ["No significant features"]
        )
    except Exception as e:
        print(f"ML analysis error: {e}")
        return MLResult(
            prediction="ERROR",
            confidence=0.0,
            top_features=[f"Error: {str(e)}"]
        )

def analyze_with_signatures(email_text: str, subject: str, sender: str) -> SignatureResult:
    """Analyze email with OWASP/CVE signatures"""
    try:
        # Combine email parts for analysis
        full_text = f"{subject} {email_text}"
        
        # Extract sender domain
        sender_domain = ""
        if '@' in sender:
            sender_domain = sender.split('@')[1].lower()
        
        # Detect signatures
        result = signature_detector.detect(full_text, sender_domain)
        
        return SignatureResult(
            matched_patterns=[p['name'] for p in result['matched_patterns']],
            matched_cves=[c['id'] for c in result['matched_cves']],
            malicious_domains=result['malicious_domains'],
            confidence=result['confidence']
        )
    except Exception as e:
        print(f"Signature analysis error: {e}")
        return SignatureResult(
            matched_patterns=[],
            matched_cves=[],
            malicious_domains=[],
            confidence=0.0
        )

def analyze_with_ollama_rag(email_data: Dict) -> OllamaResult:
    """Analyze email with RAG-enhanced Ollama"""
    try:
        # Retrieve similar examples from RAG knowledge base
        email_text = f"{email_data.get('subject', '')} {email_data.get('body', '')}"
        similar_examples = rag_system.retrieve_similar(email_text, top_k=3)
        
        # Generate enhanced prompt with context
        enhanced_prompt = rag_system.generate_enhanced_prompt(email_data, similar_examples)
        
        # Call Ollama with enhanced prompt
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": enhanced_prompt,
                "stream": False,
                "format": "json"
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON from Ollama's 'response' field
        analysis_data = json.loads(result['response'])
        
        return OllamaResult(
            summary=analysis_data.get('summary', 'No summary provided'),
            indicators=analysis_data.get('indicators', []),
            confidence=float(analysis_data.get('confidence', 0.0)),
            riskLevel=analysis_data.get('riskLevel', 'UNKNOWN'),
            similar_examples=[{
                'example': ex['example'][:100] + '...',
                'type': ex['type'],
                'similarity': ex['similarity_score']
            } for ex in similar_examples]
        )
    except Exception as e:
        print(f"Ollama analysis error: {e}")
        return OllamaResult(
            summary=f"Analysis failed: {str(e)}",
            indicators=["System Error"],
            confidence=0.0,
            riskLevel="UNKNOWN",
            similar_examples=[]
        )

def combine_analysis_results(ml_result: MLResult, sig_result: SignatureResult, ollama_result: OllamaResult) -> AnalysisResult:
    """Combine results from all three detection layers"""
    
    # Calculate weighted confidence
    # ML: 30%, Signatures: 40%, Ollama: 30%
    combined_confidence = (
        ml_result.confidence * 0.3 +
        sig_result.confidence * 0.4 +
        ollama_result.confidence * 0.3
    )
    
    # Determine overall risk level
    risk_scores = {
        'SAFE': 0,
        'SUSPICIOUS': 1,
        'MALICIOUS': 2,
        'UNKNOWN': 0
    }
    
    # Count votes for each risk level
    votes = []
    if ml_result.prediction == "PHISHING":
        votes.append('MALICIOUS')
    elif ml_result.prediction == "LEGITIMATE":
        votes.append('SAFE')
    
    if sig_result.confidence > 0.7:
        votes.append('MALICIOUS')
    elif sig_result.confidence > 0.3:
        votes.append('SUSPICIOUS')
    else:
        votes.append('SAFE')
    
    votes.append(ollama_result.riskLevel)
    
    # Majority vote with tie-breaking
    vote_counts = {level: votes.count(level) for level in set(votes)}
    final_risk_level = max(vote_counts, key=vote_counts.get)
    
    # If there's a tie, use the highest risk level
    if list(vote_counts.values()).count(max(vote_counts.values())) > 1:
        final_risk_level = max(vote_counts.keys(), key=lambda x: risk_scores.get(x, 0))
    
    # Combine indicators
    all_indicators = []
    all_indicators.extend(ml_result.top_features)
    all_indicators.extend(sig_result.matched_patterns)
    all_indicators.extend(sig_result.matched_cves)
    all_indicators.extend(sig_result.malicious_domains)
    all_indicators.extend(ollama_result.indicators)
    
    # Create summary
    summary = f"Multi-layer analysis: {final_risk_level}. "
    if ml_result.prediction == "PHISHING":
        summary += f"ML detected phishing ({ml_result.confidence:.0%}). "
    if sig_result.matched_patterns:
        summary += f"Matched {len(sig_result.matched_patterns)} OWASP patterns. "
    if sig_result.matched_cves:
        summary += f"Matched {len(sig_result.matched_cves)} CVE campaigns. "
    summary += ollama_result.summary
    
    return AnalysisResult(
        summary=summary,
        indicators=all_indicators[:10],  # Limit to top 10 indicators
        confidence=combined_confidence,
        riskLevel=final_risk_level,
        ml_analysis=ml_result,
        signature_analysis=sig_result,
        ollama_analysis=ollama_result
    )

@app.get("/api/emails", response_model=List[Email])
def get_emails():
    """Fetches emails from Mailpit and merges with local analysis cache"""
    try:
        response = requests.get(f"{MAILPIT_API_URL}/messages", timeout=5)
        response.raise_for_status()
        data = response.json()
        messages = data.get("messages", [])
        
        enriched_messages = []
        for msg in messages:
            msg_id = msg.get("ID")
            email = Email(**msg)
            
            if msg_id in analysis_cache:
                email.analysis = analysis_cache[msg_id]
                
            enriched_messages.append(email)
            
        return enriched_messages
    except requests.exceptions.ConnectionError:
        print("Could not connect to Mailpit. Returning empty list.")
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/{message_id}", response_model=AnalysisResult)
def analyze_email(message_id: str):
    """Triggers multi-layer analysis for a specific email ID"""
    try:
        # Fetch full email content from Mailpit
        response = requests.get(f"{MAILPIT_API_URL}/message/{message_id}/raw", timeout=5)
        response.raise_for_status()
        raw_content = response.text
        
        # Also get structured data
        response2 = requests.get(f"{MAILPIT_API_URL}/message/{message_id}", timeout=5)
        response2.raise_for_status()
        email_data = response2.json()
        
        # Extract email parts
        subject = email_data.get('Subject', '')
        sender = email_data.get('From', {}).get('Address', '')
        body = email_data.get('Text', '') or email_data.get('HTML', '')
        
        # Run all three detection layers
        print(f"🔍 Analyzing email {message_id}...")
        
        ml_result = analyze_with_ml(body, subject, sender)
        print(f"  ✓ ML: {ml_result.prediction} ({ml_result.confidence:.0%})")
        
        sig_result = analyze_with_signatures(body, subject, sender)
        print(f"  ✓ Signatures: {len(sig_result.matched_patterns)} patterns, {len(sig_result.matched_cves)} CVEs")
        
        ollama_result = analyze_with_ollama_rag({
            'from': sender,
            'to': email_data.get('To', [{}])[0].get('Address', ''),
            'subject': subject,
            'body': body
        })
        print(f"  ✓ Ollama: {ollama_result.riskLevel} ({ollama_result.confidence:.0%})")
        
        # Combine results
        final_result = combine_analysis_results(ml_result, sig_result, ollama_result)
        print(f"  ✅ Final: {final_result.riskLevel} ({final_result.confidence:.0%})")
        
        # Cache result
        analysis_cache[message_id] = final_result
        
        return final_result
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ml_model_loaded": ml_model is not None,
        "rag_system": rag_stats,
        "signature_detector": "active"
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Multi-Layer Phishing Detection Backend")
    print("=" * 60)
    print(f"📧 Mailpit API: {MAILPIT_API_URL}")
    print(f"🤖 Ollama API: {OLLAMA_API_URL}")
    print(f"📊 ML Model: {'Loaded' if ml_model else 'Not Available'}")
    print(f"🔍 RAG System: {rag_stats['total_examples']} examples")
    print(f"🛡️  Signature Detector: Active")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
