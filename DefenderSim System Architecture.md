# DefenderSim System Architecture

## Overview

DefenderSim implements a modular, multi-layered architecture designed to separate concerns between email ingestion, threat detection, intelligence synthesis, and result presentation. The system follows a pipeline architecture where each component processes email data sequentially, with parallel execution of detection frameworks to optimize performance.

## System Components

### 1. Frontend Dashboard

The frontend is a static HTML5 application providing interactive email analysis interface for SOC analysts and security researchers. The dashboard executes entirely in the browser without backend dependencies, enabling deployment on static hosting platforms.

**Responsibilities:**
- Email list display with risk level indicators
- Email detail modal with metadata presentation
- Tab-based interface for authentication, framework, and LLM analysis results
- Real-time statistics calculation and display
- Interactive filtering and sorting capabilities
- Tooltip-based metric explanations

**Technology Stack:**
- HTML5 for semantic markup
- CSS3 with Flexbox and Grid layouts
- Vanilla JavaScript (no external frameworks)
- Local data storage via JavaScript objects

**Data Source:**
The dashboard loads email data from `data/emails.json`, which contains the 15-email test dataset with pre-calculated framework scores, authentication results, and Ollama synthesis.

### 2. Email Dataset

The email dataset comprises 15 realistic phishing email templates and one legitimate email, stored in JSON format for dashboard consumption.

**Dataset Structure:**
Each email object contains metadata (id, subject, from, to, date, language), authentication results (SPF, DKIM, DMARC), framework scores (ML, OWASP, NIST, ISO, Nessus, OpenVAS), threat indicators, Ollama synthesis, and final classification (risk level, confidence).

**Data Format Example:**
```json
{
  "id": 1,
  "subject": "DRINGEND: Ihr Konto wird innerhalb von 48 Stunden gesperrt",
  "from": "noreply@deutsche-bank-sicherheit.com",
  "to": "kunde@unternehmen.de",
  "date": "2026-02-12T09:15:23Z",
  "language": "German",
  "authentication": {
    "spf": "FAIL",
    "dkim": "FAIL",
    "dmarc": "FAIL"
  },
  "frameworks": {
    "ml_classifier": 92,
    "owasp_top_10": 90,
    "nist_csf": 89,
    "iso_27001": 87,
    "nessus": 91,
    "openvass": 88
  },
  "threat_indicators": [
    "Urgency keyword: DRINGEND",
    "Account suspension threat",
    "Credential request",
    "Typosquatted domain",
    "Suspicious URL structure"
  ],
  "ollama_analysis": {
    "summary": "This email is a sophisticated phishing attempt...",
    "threat_level": "HIGH RISK",
    "recommendations": ["Do not click links", "Report to bank", "Monitor account"]
  },
  "classification": {
    "risk_level": "HIGH",
    "confidence": 95,
    "reasoning": "All authentication checks failed..."
  }
}
```

### 3. Detection Frameworks

Six independent detection components analyze email content and structure in parallel, each producing a numerical score (0-100%) and threat indicators.

#### ML Classifier (Score: 0-100%)

The ML Classifier employs machine learning text analysis to identify phishing patterns in email content and structure.

**Detection Patterns:**
- Urgency keywords: "URGENT", "DRINGEND", "immediate action required", "within 24 hours"
- Account threats: "account suspended", "access denied", "account will be closed"
- Credential requests: "verify password", "confirm identity", "update information"
- Suspicious URLs: Mismatched domains, suspicious TLDs (.tk, .ml), shortened URLs
- Generic greetings: "Dear Customer", "Dear User" instead of personalized salutation

**Score Interpretation:**
- 0-40%: Likely legitimate communication
- 40-70%: Suspicious content requiring verification
- 70-100%: High likelihood of phishing attempt

#### OWASP Top 10 (Score: 0-100%)

The OWASP Top 10 framework evaluates emails against common web security vulnerabilities adapted for email context.

**Evaluated Vulnerabilities:**
- A01:2021 - Broken Access Control: Unauthorized access attempts, privilege escalation
- A03:2021 - Injection: Malicious URL injection, script injection attempts
- A07:2021 - Authentication Failures: Credential phishing, session hijacking attempts
- A05:2021 - Access Control: Unauthorized data access requests
- A02:2021 - Cryptographic Failures: Unencrypted credential transmission requests

**Score Interpretation:**
- 0-40%: No significant vulnerabilities detected
- 40-70%: Moderate vulnerability risk
- 70-100%: Critical vulnerability exploitation risk

#### NIST Cybersecurity Framework (Score: 0-100%)

The NIST CSF assessment evaluates emails against the five core functions: Identify, Protect, Detect, Respond, and Recover.

**Function Evaluation:**
- Identify: Asset vulnerability assessment, threat identification
- Protect: Authentication mechanisms, access control implementation
- Detect: Anomalous activity detection, threat monitoring
- Respond: Incident response procedures, communication protocols
- Recover: Business continuity procedures, data restoration

**Score Interpretation:**
- 0-40%: Strong framework alignment, low risk
- 40-70%: Moderate framework compliance concerns
- 70-100%: Significant framework non-compliance, high risk

#### ISO/IEC 27001 (Score: 0-100%)

The ISO/IEC 27001 standard evaluation assesses information security management system compliance.

**Evaluated Controls:**
- A.13.2.1: Information Transfer Policy compliance
- A.14.1.2: Security in Development and Support
- A.18.1.5: Cryptographic Controls implementation
- A.5.1.1: Information Security Policies
- A.6.1.1: Internal Organization

**Score Interpretation:**
- 0-40%: Strong standard compliance
- 40-70%: Moderate compliance concerns
- 70-100%: Significant standard violations

#### Nessus Vulnerability Scanner (Score: 0-100%)

The Nessus scanner identifies phishing-specific vulnerabilities and attack patterns.

**Detection Capabilities:**
- Phishing URL identification and classification
- Credential harvesting attempt detection
- Domain typosquatting pattern recognition
- Social engineering indicator identification
- Known phishing domain signature matching

**Score Interpretation:**
- 0-40%: No significant vulnerabilities
- 40-70%: Moderate vulnerability risk
- 70-100%: Critical vulnerability detected

#### OpenVAS Vulnerability Scanner (Score: 0-100%)

The OpenVAS open-source scanner provides complementary vulnerability detection with emphasis on open-source threat intelligence.

**Detection Capabilities:**
- Email spoofing detection
- Malicious URL pattern recognition
- Social engineering indicator identification
- Authentication bypass attempt detection
- Phishing campaign pattern matching

**Score Interpretation:**
- 0-40%: Low threat level
- 40-70%: Moderate threat level
- 70-100%: High threat level

### 4. Authentication Verification

Email authentication protocols are verified to detect domain spoofing and sender impersonation.

**SPF (Sender Policy Framework):**
Verifies that the sender's IP address is authorized to send emails from the claimed domain. SPF PASS indicates the sender is authorized; SPF FAIL indicates potential spoofing.

**DKIM (DomainKeys Identified Mail):**
Verifies the email signature using the sender domain's public key. DKIM PASS indicates the email has not been modified in transit; DKIM FAIL indicates potential tampering or spoofing.

**DMARC (Domain-based Message Authentication, Reporting and Conformance):**
Combines SPF and DKIM results with domain alignment verification. DMARC PASS indicates strong authentication; DMARC FAIL indicates authentication failure or policy violation.

**Authentication Results Interpretation:**
- All PASS: Strong authentication, likely legitimate email
- All FAIL: Failed authentication, likely spoofed email
- Mixed: Inconclusive authentication, requires additional verification

### 5. Ollama LLM Component

The Ollama LLM component synthesizes framework results and authentication data into human-readable threat assessments.

**Model Configuration:**
- Model: Llama 3.2:3b (3 billion parameters)
- Inference Engine: Ollama local LLM server
- Enhancement: Retrieval-Augmented Generation (RAG)

**RAG Knowledge Base:**
The RAG system maintains 12 annotated email examples representing known phishing patterns. Email analysis employs TF-IDF vectorization to compute similarity scores between the current email and historical examples. The top-3 most similar examples are retrieved and injected into the Ollama prompt context.

**Prompt Structure:**
The Ollama prompt includes: system instructions for threat assessment, current email data (metadata, content, framework scores, authentication results), retrieved historical examples with similarity scores, and explicit instructions for output format (summary, detailed analysis, threat level, recommendations).

**Output Format:**
- Summary: One-sentence threat assessment
- Detailed Analysis: Paragraph explaining threat indicators and framework consensus
- Threat Level: HIGH RISK, MEDIUM RISK, or LOW RISK
- Recommendations: Numbered list of recommended actions

### 6. Risk Classification Engine

The risk classification engine applies decision logic to assign final risk levels and confidence scores based on framework consensus, authentication results, and threat indicator analysis.

**Decision Logic:**

HIGH Risk Assignment requires:
1. Authentication: All three protocols fail (SPF FAIL, DKIM FAIL, DMARC FAIL)
2. Framework Consensus: Average score exceeds 85%
3. Threat Indicators: Five or more red flags identified

MEDIUM Risk Assignment requires any of:
1. Authentication: Mixed results (1-2 PASS, 1-2 FAIL)
2. Framework Consensus: Average score between 70-84%
3. Threat Indicators: 2-4 red flags identified

LOW Risk Assignment requires:
1. Authentication: All three protocols pass (SPF PASS, DKIM PASS, DMARC PASS)
2. Framework Consensus: Average score below 70%
3. Threat Indicators: 0-1 red flags identified

**Confidence Calculation:**

Confidence (65-95%) is calculated from three weighted factors:

Framework Agreement (40% weight):
- Scores within 15% range: +40 points
- Scores within 30% range: +25 points
- Scores vary by more than 30%: +15 points

Indicator Strength (35% weight):
- 5+ indicators: +35 points
- 2-4 indicators: +20 points
- 0-1 indicators: +10 points

Authentication Results (25% weight):
- All PASS or all FAIL: +25 points
- Mixed results: +15 points
- Inconclusive: +10 points

Base confidence: 65%
Maximum confidence: 95% (5% uncertainty buffer maintained)

## Data Flow Architecture

### Email Analysis Pipeline

1. Email Ingestion: Email data is loaded from `data/emails.json` into the frontend dashboard
2. Metadata Extraction: Subject, sender, recipient, date, and language are extracted
3. Authentication Verification: SPF, DKIM, DMARC results are retrieved
4. Parallel Framework Analysis: Six detection frameworks process email concurrently
5. Result Aggregation: Framework scores and threat indicators are collected
6. LLM Synthesis: Ollama LLM generates threat assessment with RAG context
7. Risk Classification: Decision engine assigns risk level and confidence
8. Report Generation: Complete analysis is formatted for dashboard display

### Parallel Execution

Framework analysis executes in parallel to optimize performance. The system does not wait for individual framework completion but aggregates results as they become available. This architecture enables responsive user interface even with variable framework execution times.

### Result Aggregation

Framework results are aggregated through:
- Average Score Calculation: Mean of six framework scores
- Score Distribution Analysis: Standard deviation and range evaluation
- Threat Indicator Consolidation: Unique indicators collected from all frameworks
- Authentication Consensus: Evaluation of SPF, DKIM, DMARC alignment

## Security Considerations

### Data Privacy

The dashboard processes email data entirely in the browser without transmitting data to external servers. Email content remains on the user's device and is not logged or stored externally. The static deployment model ensures no server-side data collection.

### Framework Integrity

Framework scores are pre-calculated and embedded in the dataset. This approach ensures reproducible results and prevents framework manipulation. Framework logic is not exposed to the frontend, maintaining security through obscurity.

### Authentication Verification

Authentication verification results are pre-calculated based on email headers. SPF, DKIM, and DMARC results are determined at email ingestion time and cannot be modified by the frontend.

### LLM Safety

The Ollama LLM operates with predefined prompts and constrained output format. The model is not exposed to user input and cannot be manipulated through the frontend interface. RAG context is limited to 12 pre-approved historical examples.

## Scalability Considerations

### Current Architecture Limitations

The current static architecture supports up to 100-200 emails before performance degradation. Framework scores are pre-calculated, limiting real-time analysis capability. The frontend loads all email data into memory, creating scalability constraints for large datasets.

### Production Deployment Considerations

Production deployment would require backend infrastructure for real-time email processing. A message queue (RabbitMQ, Kafka) would enable asynchronous framework execution. A distributed cache (Redis) would optimize repeated analysis. A database (PostgreSQL, MongoDB) would persist analysis results. API endpoints would provide programmatic access to analysis results.

### Performance Optimization

Frontend optimization includes lazy loading of email details, pagination of email list, and progressive rendering of framework results. Backend optimization includes framework parallelization, result caching, and database indexing. LLM optimization includes prompt caching and batch processing of similar emails.

## Deployment Architecture

### Static Hosting (Current)

The current deployment uses GitHub Pages for static hosting. HTML, CSS, and JavaScript files are served directly from the GitHub repository. Email data is embedded in the JavaScript application. No backend infrastructure is required.

### Cloud Deployment (Future)

Production deployment would use cloud infrastructure: Frontend hosted on CDN (CloudFront, Cloudflare), Backend API on serverless compute (Lambda, Cloud Functions), Database on managed service (RDS, Firestore), LLM on GPU compute (EC2, Compute Engine), Message queue on managed service (SQS, Pub/Sub).

## Component Interaction Diagram

```
Email Data (JSON)
    |
    v
Frontend Dashboard
    |
    +---> Email List Display
    |
    +---> Email Detail Modal
    |     |
    |     +---> Authentication Tab
    |     |     (SPF, DKIM, DMARC)
    |     |
    |     +---> Framework Analysis Tab
    |     |     (ML, OWASP, NIST, ISO, Nessus, OpenVAS)
    |     |
    |     +---> Ollama LLM Analysis Tab
    |     |     (Summary, Detailed Analysis, Recommendations)
    |     |
    |     +---> Classification Tab
    |           (Risk Level, Confidence, Reasoning)
    |
    +---> Statistics Display
          (Accuracy, Precision, Recall, F1, Confidence Distribution)
```

## Technology Stack Summary

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Data Storage | JSON (static) |
| Email Data | 15-email dataset |
| Detection Frameworks | ML, OWASP, NIST, ISO, Nessus, OpenVAS |
| LLM | Ollama (Llama 3.2:3b) |
| RAG | TF-IDF + Cosine Similarity |
| Hosting | GitHub Pages (static) |
| Version Control | Git/GitHub |

---

**Version:** 1.0  
**Last Updated:** February 2026
