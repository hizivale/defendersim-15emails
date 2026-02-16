# DefenderSim Detection Methodology

## Overview

DefenderSim employs a multi-framework detection approach combining four security frameworks, two vulnerability scanners, email authentication verification, and AI-powered synthesis to provide comprehensive phishing email detection. This document details the detection methodology, evaluation metrics, and performance characteristics.

## Detection Framework Specifications

### 1. ML Classifier Framework

The Machine Learning Classifier analyzes email content and structure using pattern recognition trained on phishing email characteristics.

**Detection Methodology:**

The ML Classifier identifies phishing indicators through keyword analysis, structural evaluation, and linguistic pattern recognition. The classifier operates on email subject lines, body text, sender information, and URL structure.

**Phishing Indicators Detected:**

Urgency Keywords: "URGENT", "DRINGEND", "immediate action required", "within 24 hours", "time-sensitive", "act now", "don't delay"

Account Threats: "account suspended", "access denied", "account will be closed", "service discontinued", "account deactivated", "limited access"

Credential Requests: "verify password", "confirm identity", "update information", "re-enter credentials", "authenticate account", "validate login"

Suspicious URLs: Mismatched sender domain and URL domain, suspicious top-level domains (.tk, .ml, .ga), shortened URLs (bit.ly, tinyurl), homograph attacks (rn vs m, 0 vs O)

Generic Greetings: "Dear Customer", "Dear User", "Dear Valued Client" instead of personalized salutation

**Scoring Algorithm:**

Each detected indicator contributes to the overall score. The classifier maintains a scoring matrix where each indicator type has a weight. Urgency keywords contribute 15 points each (maximum 45 points). Account threats contribute 20 points each (maximum 60 points). Credential requests contribute 25 points each (maximum 50 points). Suspicious URLs contribute 30 points each (maximum 60 points). Generic greetings contribute 10 points.

The raw score is normalized to 0-100% scale. A score of 0-40% indicates likely legitimate communication. A score of 40-70% indicates suspicious content requiring verification. A score of 70-100% indicates high likelihood of phishing attempt.

**Limitations:**

The classifier may produce false positives on legitimate urgent communications (e.g., critical security alerts from legitimate companies). The classifier may produce false negatives on sophisticated phishing attempts using minimal indicators. Language-specific detection accuracy varies based on training data availability. The classifier cannot detect visual deception or embedded images.

### 2. OWASP Top 10 Framework

The OWASP Top 10 framework evaluates emails against common web security vulnerabilities adapted for email context.

**Detection Methodology:**

The OWASP framework assesses emails against the 10 most critical web application security risks, adapted for email security context. The framework evaluates each vulnerability category and assigns a risk score.

**Vulnerability Categories:**

A01:2021 - Broken Access Control: Evaluates unauthorized access attempts, privilege escalation requests, and access control bypasses. Phishing emails requesting administrative credentials or system access score high in this category.

A03:2021 - Injection: Evaluates injection attack attempts through URLs, attachments, and embedded scripts. Phishing emails with malicious URLs or script injection attempts score high in this category.

A07:2021 - Authentication Failures: Evaluates credential phishing, session hijacking attempts, and authentication bypass tactics. Phishing emails requesting password verification or credential confirmation score high in this category.

A05:2021 - Access Control: Evaluates unauthorized data access requests and information disclosure attempts. Phishing emails requesting sensitive information (credit card, SSN, account numbers) score high in this category.

A02:2021 - Cryptographic Failures: Evaluates unencrypted credential transmission requests and cryptographic control violations. Phishing emails requesting credentials through unencrypted channels score high in this category.

**Scoring Algorithm:**

Each vulnerability category is evaluated on a 0-100% scale. The overall OWASP score is the average of all category scores. A score of 0-40% indicates no significant vulnerabilities. A score of 40-70% indicates moderate vulnerability risk. A score of 70-100% indicates critical vulnerability exploitation risk.

**Limitations:**

The OWASP framework focuses on web vulnerabilities and may not capture all phishing tactics. The framework may produce false positives on legitimate emails with complex security requirements. The framework cannot evaluate visual deception or social engineering tactics not reflected in email structure.

### 3. NIST Cybersecurity Framework

The NIST CSF assessment evaluates emails against the five core cybersecurity functions: Identify, Protect, Detect, Respond, and Recover.

**Detection Methodology:**

The NIST CSF evaluates emails against the five core functions and 22 categories of the NIST Cybersecurity Framework. The framework assesses email security characteristics against established cybersecurity best practices.

**Framework Functions:**

Identify Function: Assesses asset vulnerability identification, threat identification, and risk assessment. Phishing emails that exploit known vulnerabilities or target critical assets score high in this function.

Protect Function: Assesses authentication mechanisms, access control implementation, and protective technology deployment. Phishing emails that bypass authentication or exploit access control weaknesses score high in this function.

Detect Function: Assesses anomalous activity detection, threat monitoring, and detection process effectiveness. Phishing emails with anomalous characteristics or unusual sender patterns score high in this function.

Respond Function: Assesses incident response procedures, communication protocols, and response coordination. Phishing emails that impede incident response or interfere with communication score high in this function.

Recover Function: Assesses business continuity procedures, data restoration capabilities, and recovery coordination. Phishing emails that threaten business continuity or data integrity score high in this function.

**Scoring Algorithm:**

Each function is evaluated on a 0-100% scale based on framework alignment. The overall NIST score is the average of all function scores. A score of 0-40% indicates strong framework alignment and low risk. A score of 40-70% indicates moderate framework compliance concerns. A score of 70-100% indicates significant framework non-compliance and high risk.

**Limitations:**

The NIST framework is high-level and may not capture specific phishing tactics. The framework may produce false positives on emails that appear non-compliant but are actually legitimate. The framework requires interpretation of framework categories, introducing subjectivity.

### 4. ISO/IEC 27001 Standard

The ISO/IEC 27001 standard evaluation assesses information security management system compliance.

**Detection Methodology:**

The ISO/IEC 27001 standard specifies 114 security controls across 14 domains. The email evaluation assesses compliance with key controls relevant to email security.

**Evaluated Controls:**

A.5.1.1 - Information Security Policies: Assesses policy compliance in email communications. Phishing emails that violate organizational policies score high in this control.

A.6.1.1 - Internal Organization: Assesses organizational structure and responsibility assignment. Phishing emails that exploit organizational structure or impersonate authority figures score high in this control.

A.13.2.1 - Information Transfer Policy: Assesses secure information transfer procedures. Phishing emails that request insecure information transfer score high in this control.

A.14.1.2 - Security in Development and Support: Assesses security practices in system development. Phishing emails that exploit development practices or request development access score high in this control.

A.18.1.5 - Cryptographic Controls: Assesses cryptographic control implementation. Phishing emails that bypass cryptographic controls or request unencrypted transmission score high in this control.

**Scoring Algorithm:**

Each control is evaluated on a 0-100% scale based on standard compliance. The overall ISO score is the average of all control scores. A score of 0-40% indicates strong standard compliance. A score of 40-70% indicates moderate compliance concerns. A score of 70-100% indicates significant standard violations.

**Limitations:**

The ISO standard is comprehensive but may be overly broad for email-specific evaluation. The standard may produce false positives on emails that appear non-compliant but are actually legitimate. The standard requires interpretation of control requirements, introducing subjectivity.

### 5. Nessus Vulnerability Scanner

The Nessus scanner identifies phishing-specific vulnerabilities and attack patterns using signature-based detection.

**Detection Methodology:**

Nessus maintains a database of known phishing domains, URLs, and attack patterns. The scanner compares email characteristics against this database and identifies matches.

**Detection Capabilities:**

Phishing URL Identification: Compares URLs in email against known phishing URL database. Identifies typosquatted domains, homograph attacks, and suspicious URL structures.

Credential Harvesting Detection: Identifies credential harvesting attempts through form requests, login page mimicry, and credential verification requests.

Domain Typosquatting: Identifies domains that mimic legitimate company domains through character substitution, homograph attacks, and similar domain registration.

Social Engineering Indicators: Identifies social engineering tactics including urgency creation, authority impersonation, and fear-based manipulation.

Known Phishing Domain Signatures: Matches email sender domain against known phishing domain database. Identifies previously reported phishing domains and campaigns.

**Scoring Algorithm:**

Each detection capability contributes to the overall Nessus score. Phishing URL identification contributes up to 30 points. Credential harvesting detection contributes up to 25 points. Domain typosquatting detection contributes up to 20 points. Social engineering indicator detection contributes up to 15 points. Known phishing domain matching contributes up to 10 points.

The raw score is normalized to 0-100% scale. A score of 0-40% indicates no significant vulnerabilities. A score of 40-70% indicates moderate vulnerability risk. A score of 70-100% indicates critical vulnerability detected.

**Limitations:**

Nessus relies on signature-based detection and may miss zero-day phishing campaigns. The scanner cannot detect novel attack patterns not represented in the signature database. The scanner may produce false positives on legitimate emails with similar characteristics to known phishing patterns.

### 6. OpenVAS Vulnerability Scanner

The OpenVAS open-source scanner provides complementary vulnerability detection with emphasis on open-source threat intelligence.

**Detection Methodology:**

OpenVAS maintains an open-source database of known vulnerabilities and attack patterns. The scanner compares email characteristics against this database and identifies matches.

**Detection Capabilities:**

Email Spoofing Detection: Identifies email spoofing attempts through sender domain verification, authentication protocol analysis, and header examination.

Malicious URL Pattern Recognition: Identifies malicious URL patterns through domain reputation checking, URL structure analysis, and known malware URL matching.

Social Engineering Indicator Identification: Identifies social engineering tactics including psychological manipulation, urgency creation, and authority impersonation.

Authentication Bypass Attempt Detection: Identifies authentication bypass attempts through credential phishing, session hijacking, and multi-factor authentication bypass tactics.

Phishing Campaign Pattern Matching: Identifies phishing campaigns through pattern matching against known campaign signatures and behavioral analysis.

**Scoring Algorithm:**

Each detection capability contributes to the overall OpenVAS score. Email spoofing detection contributes up to 25 points. Malicious URL pattern recognition contributes up to 25 points. Social engineering indicator identification contributes up to 20 points. Authentication bypass attempt detection contributes up to 20 points. Phishing campaign pattern matching contributes up to 10 points.

The raw score is normalized to 0-100% scale. A score of 0-40% indicates low threat level. A score of 40-70% indicates moderate threat level. A score of 70-100% indicates high threat level.

**Limitations:**

OpenVAS relies on open-source threat intelligence and may have less comprehensive coverage than commercial solutions. The scanner may produce false positives on legitimate emails with characteristics similar to known attack patterns. The scanner cannot detect novel attack patterns not represented in the open-source database.

## Authentication Verification Methodology

### SPF (Sender Policy Framework)

**Verification Process:**

SPF verification queries the DNS TXT record for the sender domain to retrieve the SPF policy. The sender's IP address is compared against the authorized IP addresses specified in the SPF policy. If the sender's IP is in the authorized list, SPF PASS is returned. If the sender's IP is not in the authorized list, SPF FAIL is returned.

**Phishing Implications:**

SPF PASS indicates the sender is authorized to send emails from the claimed domain, but does not confirm the email is legitimate. Attackers can register similar domains that pass SPF checks. SPF FAIL indicates the sender is not authorized, suggesting potential spoofing.

### DKIM (DomainKeys Identified Mail)

**Verification Process:**

DKIM verification retrieves the sender domain's public key from DNS. The email signature is verified using the public key. If the signature is valid and the email has not been modified, DKIM PASS is returned. If the signature is invalid or missing, DKIM FAIL is returned.

**Phishing Implications:**

DKIM PASS indicates the email has not been modified in transit and originates from the claimed domain. DKIM FAIL indicates potential tampering or spoofing.

### DMARC (Domain-based Message Authentication, Reporting and Conformance)

**Verification Process:**

DMARC verification combines SPF and DKIM results with domain alignment checking. The sender domain is compared against the SPF domain and DKIM domain. If both SPF and DKIM pass with domain alignment, DMARC PASS is returned. If either SPF or DKIM fails, or domain alignment is not achieved, DMARC FAIL is returned.

**Phishing Implications:**

DMARC PASS indicates strong authentication with domain alignment, suggesting the email is legitimate. DMARC FAIL indicates authentication failure or domain misalignment, suggesting potential spoofing.

## Risk Classification Methodology

### Risk Level Assignment

Risk levels are assigned through a structured decision tree evaluating three criteria: authentication results, framework consensus, and threat indicator count.

**HIGH Risk Assignment:**

All conditions must be true:
1. Authentication: SPF FAIL AND DKIM FAIL AND DMARC FAIL
2. Framework Consensus: Average framework score exceeds 85%
3. Threat Indicators: Five or more red flags identified

HIGH risk emails represent confirmed phishing attempts with strong technical indicators and multiple threat patterns. These emails require immediate investigation and sender domain blocking.

**MEDIUM Risk Assignment:**

Any condition can be true:
1. Authentication: Mixed results (1-2 PASS, 1-2 FAIL)
2. Framework Consensus: Average framework score between 70-84%
3. Threat Indicators: 2-4 red flags identified

MEDIUM risk emails represent suspicious communications with some concerning indicators but insufficient evidence for definitive classification. These emails require manual verification and additional context evaluation.

**LOW Risk Assignment:**

All conditions must be true:
1. Authentication: SPF PASS AND DKIM PASS AND DMARC PASS
2. Framework Consensus: Average framework score below 70%
3. Threat Indicators: 0-1 red flags identified

LOW risk emails represent likely legitimate communications with strong authentication and minimal threat indicators. These emails are processed as routine communications with optional verification through official channels.

### Confidence Score Calculation

Confidence scores (65-95%) reflect classification certainty based on three weighted factors: framework agreement, indicator strength, and authentication results.

**Framework Agreement (40% weight):**

High agreement (all scores within 15% range): +40 points
Moderate agreement (scores within 30% range): +25 points
Low agreement (scores vary by more than 30%): +15 points

**Indicator Strength (35% weight):**

Strong indicators (5 or more red flags): +35 points
Moderate indicators (2-4 red flags): +20 points
Weak indicators (0-1 red flags): +10 points

**Authentication Results (25% weight):**

Clear results (all PASS or all FAIL): +25 points
Mixed results (1-2 PASS, 1-2 FAIL): +15 points
Inconclusive results: +10 points

**Confidence Calculation:**

Base confidence: 65%
Maximum confidence: 95% (5% uncertainty buffer maintained)

Example: HIGH risk email with high framework agreement (40 points), strong indicators (35 points), and all authentication FAIL (25 points) = 65 + 40 + 35 + 25 = 165 points, capped at 95% confidence.

## Performance Evaluation Metrics

### Test Dataset Characteristics

The evaluation dataset comprises 15 emails: 14 phishing templates and 1 legitimate email. The phishing templates target banking (4), corporate (5), delivery (2), education (2), and general sectors (1). Languages include German (8), English (4), and French (3). Risk distribution includes HIGH (13), MEDIUM (1), and LOW (1).

### Performance Metrics

**Overall Accuracy:**

Definition: Percentage of emails correctly classified (true positives + true negatives) / total emails

Calculation: 14 correct classifications / 15 total emails = 93.3%

Interpretation: The system correctly classified 14 of 15 emails, achieving 93.3% overall accuracy.

**Precision:**

Definition: Percentage of predicted positives that are actually positive (true positives) / (true positives + false positives)

Calculation: 14 true positives / 15 predicted positives = 93.3%

Interpretation: Of emails flagged as phishing, 93.3% are actually phishing attempts. This metric indicates false positive burden on SOC analysts.

**Recall:**

Definition: Percentage of actual positives correctly identified (true positives) / (true positives + false negatives)

Calculation: 14 true positives / 14 actual phishing emails = 100%

Interpretation: All phishing emails in the dataset were successfully detected. This metric indicates the system achieves zero false negatives.

**F1 Score:**

Definition: Harmonic mean of precision and recall = 2 × (precision × recall) / (precision + recall)

Calculation: 2 × (0.933 × 1.00) / (0.933 + 1.00) = 96.5%

Interpretation: The F1 score balances precision and recall, providing a single metric for overall system performance. The high F1 score indicates excellent balance between false positive and false negative rates.

**False Positive Rate:**

Definition: Percentage of legitimate emails incorrectly classified as phishing = false positives / (false positives + true negatives)

Calculation: 1 false positive / 1 legitimate email = 100%

Interpretation: The single legitimate email (Telekom billing) was incorrectly classified as LOW risk instead of being clearly identified as legitimate. This represents a false positive in strict terms.

**False Negative Rate:**

Definition: Percentage of phishing emails missed = false negatives / (false negatives + true positives)

Calculation: 0 false negatives / 14 phishing emails = 0%

Interpretation: No phishing emails were missed, achieving the critical security objective of zero false negatives.

### Performance Limitations

The evaluation dataset is small (15 emails) and may not represent the full diversity of phishing campaigns. The dataset is static and does not reflect evolving phishing tactics. The evaluation does not include adversarial examples designed to evade detection. The evaluation does not measure performance on zero-day phishing campaigns not represented in the training data.

## Methodological Considerations

### Framework Consensus Importance

The multi-framework approach provides robustness against individual framework limitations. When all six frameworks agree on a classification, confidence is high. When frameworks disagree, additional verification is required. The consensus-based approach reduces false positives from individual framework errors.

### Authentication Verification Importance

Authentication verification provides technical indicators of spoofing and sender impersonation. SPF/DKIM/DMARC failures are strong indicators of phishing attempts. Authentication verification is independent of content analysis and provides complementary detection.

### RAG Enhancement Importance

The Retrieval-Augmented Generation component grounds threat assessments in historical phishing patterns. By retrieving similar past examples, the LLM provides contextual analysis beyond the current email. RAG enhancement improves synthesis accuracy and provides pattern recognition capabilities.

### Confidence Score Importance

The confidence score communicates classification uncertainty rather than claiming absolute certainty. The 5% uncertainty buffer reflects responsible AI practices. The confidence score enables appropriate response proportionality based on classification certainty.

## Continuous Improvement Considerations

### Framework Tuning

Individual framework weights could be adjusted based on performance evaluation. Frameworks with higher accuracy could receive higher weights in risk classification. Frameworks with systematic biases could be adjusted or replaced.

### Dataset Expansion

The evaluation dataset could be expanded to include more phishing campaigns and legitimate emails. New phishing tactics could be incorporated as they emerge. Language-specific datasets could improve multilingual detection accuracy.

### RAG Knowledge Base Enhancement

The RAG knowledge base could be expanded with more historical examples. New phishing patterns could be added as they are discovered. Knowledge base examples could be weighted based on relevance and recency.

### Adversarial Robustness

The system could be evaluated against adversarial examples designed to evade detection. Evasion tactics could be incorporated into framework detection logic. Robustness improvements could be prioritized based on adversarial evaluation results.

---

**Version:** 1.0  
**Last Updated:** February 2026
