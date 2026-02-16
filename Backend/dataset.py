"""
Generate synthetic phishing and legitimate email dataset for training
"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

# Phishing indicators
PHISHING_SENDERS = [
    "security@paypaI.com",  # Fake PayPal (capital i)
    "noreply@amazon-verify.ru",
    "support@microsoft-security.net",
    "admin@bank-alert.com",
    "service@apple-id-locked.com",
    "notifications@netflix-billing.org",
    "verify@google-account-suspended.com",
    "urgent@fedex-delivery.info",
    "admin@dhl-package-tracking.biz",
    "security@facebook-verify.co"
]

LEGITIMATE_SENDERS = [
    "newsletter@company.com",
    "hr@acmecorp.com",
    "support@github.com",
    "notifications@slack.com",
    "team@atlassian.com",
    "updates@linkedin.com",
    "billing@stripe.com",
    "noreply@zoom.us",
    "calendar@google.com",
    "alerts@datadog.com"
]

PHISHING_SUBJECTS = [
    "URGENT: Your account will be closed",
    "Verify your identity immediately",
    "Unusual activity detected - Action Required",
    "Your package could not be delivered",
    "Confirm your payment information",
    "Security Alert: Suspicious login attempt",
    "Your account has been suspended",
    "Important: Update your billing details",
    "Final Notice: Verify your account",
    "Wire transfer approval needed"
]

LEGITIMATE_SUBJECTS = [
    "Weekly team meeting - Thursday 2 PM",
    "Q1 Planning Document",
    "Your monthly invoice",
    "Project update: Feature release",
    "Welcome to our newsletter",
    "Meeting notes from today",
    "Code review requested",
    "System maintenance scheduled",
    "New feature announcement",
    "Team lunch next Friday"
]

PHISHING_BODIES = [
    "Dear valued customer, we detected unusual activity on your account. Click here to verify: http://verify-account-now.ru/login",
    "Your package is waiting for delivery. Pay the customs fee here: http://dhl-delivery.biz/pay?id=12345",
    "We need to confirm your identity. Please update your information immediately: http://secure-login.net/verify",
    "Your account will be suspended in 24 hours unless you verify your details: http://account-verify.com/urgent",
    "You have won $1,000,000! Claim your prize now: http://winner-claim.org/prize",
    "Important security update required. Download the patch: http://microsoft-update.net/security.exe",
    "Your payment was declined. Update your credit card: http://billing-update.com/card",
    "IRS Tax Refund: You are eligible for a $2,500 refund. Claim here: http://irs-refund.gov.ru/claim",
    "Your Netflix subscription will expire. Renew now: http://netflix-renew.org/billing",
    "CEO: I need you to wire $50,000 to our vendor immediately. Reply with confirmation."
]

LEGITIMATE_BODIES = [
    "Hi team, just a reminder about our weekly sync meeting this Thursday at 2 PM in Conference Room B. See you there!",
    "Attached is the Q1 planning document for review. Please provide feedback by Friday.",
    "Your monthly invoice for January is attached. Payment is due within 30 days.",
    "Great progress on the new feature! The release is scheduled for next Monday. Let me know if you need any support.",
    "Welcome to our monthly newsletter. This month we're covering industry trends and best practices.",
    "Thanks everyone for attending today's meeting. I've attached the notes and action items.",
    "I've submitted a pull request for the authentication feature. Could you review when you get a chance?",
    "Scheduled system maintenance will occur this Saturday from 2-4 AM EST. Services will be briefly unavailable.",
    "We're excited to announce our new collaboration feature! Check out the demo video in the link below.",
    "Team lunch next Friday at 12:30 PM at the Italian restaurant downtown. RSVP by Wednesday."
]

PHISHING_URLS = [
    "http://verify-account-now.ru",
    "http://secure-login.net",
    "http://phishing-site.com",
    "http://fake-bank.org",
    "http://malicious-link.biz"
]

LEGITIMATE_URLS = [
    "https://company.com/dashboard",
    "https://github.com/repo",
    "https://docs.google.com/document",
    "https://zoom.us/meeting",
    "https://slack.com/workspace"
]

def generate_phishing_email(index: int) -> Dict:
    """Generate a synthetic phishing email"""
    sender = random.choice(PHISHING_SENDERS)
    subject = random.choice(PHISHING_SUBJECTS)
    body = random.choice(PHISHING_BODIES)
    
    # Add urgency keywords
    urgency_words = ["urgent", "immediately", "action required", "suspended", "verify now", "final notice"]
    has_urgency = any(word in subject.lower() or word in body.lower() for word in urgency_words)
    
    # Add suspicious URLs
    url_count = random.randint(1, 3)
    urls = random.sample(PHISHING_URLS, min(url_count, len(PHISHING_URLS)))
    
    # Extract domain from sender
    sender_domain = sender.split('@')[1] if '@' in sender else ""
    
    return {
        "id": f"phish_{index}",
        "from": sender,
        "to": "user@company.com",
        "subject": subject,
        "body": body,
        "urls": urls,
        "url_count": len(urls),
        "has_urgency": has_urgency,
        "sender_domain": sender_domain,
        "has_suspicious_domain": any(ext in sender_domain for ext in [".ru", ".biz", ".info", ".org", ".net"]),
        "has_typosquatting": any(char in sender for char in ["I", "l", "0", "O"]),  # Common typosquatting chars
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        "label": "phishing"
    }

def generate_legitimate_email(index: int) -> Dict:
    """Generate a synthetic legitimate email"""
    sender = random.choice(LEGITIMATE_SENDERS)
    subject = random.choice(LEGITIMATE_SUBJECTS)
    body = random.choice(LEGITIMATE_BODIES)
    
    # Legitimate emails rarely have urgency
    urgency_words = ["urgent", "immediately", "action required", "suspended", "verify now"]
    has_urgency = any(word in subject.lower() or word in body.lower() for word in urgency_words)
    
    # Add legitimate URLs (fewer, more trusted)
    url_count = random.randint(0, 1)
    urls = random.sample(LEGITIMATE_URLS, min(url_count, len(LEGITIMATE_URLS))) if url_count > 0 else []
    
    # Extract domain from sender
    sender_domain = sender.split('@')[1] if '@' in sender else ""
    
    return {
        "id": f"legit_{index}",
        "from": sender,
        "to": "user@company.com",
        "subject": subject,
        "body": body,
        "urls": urls,
        "url_count": len(urls),
        "has_urgency": has_urgency,
        "sender_domain": sender_domain,
        "has_suspicious_domain": False,
        "has_typosquatting": False,
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        "label": "legitimate"
    }

def generate_dataset(num_phishing: int = 500, num_legitimate: int = 500) -> List[Dict]:
    """Generate complete dataset"""
    dataset = []
    
    print(f"Generating {num_phishing} phishing emails...")
    for i in range(num_phishing):
        dataset.append(generate_phishing_email(i))
    
    print(f"Generating {num_legitimate} legitimate emails...")
    for i in range(num_legitimate):
        dataset.append(generate_legitimate_email(i))
    
    # Shuffle dataset
    random.shuffle(dataset)
    
    return dataset

if __name__ == "__main__":
    print("=== Email Dataset Generator ===\n")
    
    # Generate dataset
    dataset = generate_dataset(500, 500)
    
    # Save to JSON
    output_file = "training_dataset.json"
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n✅ Dataset generated: {len(dataset)} emails")
    print(f"📁 Saved to: {output_file}")
    
    # Print statistics
    phishing_count = sum(1 for email in dataset if email['label'] == 'phishing')
    legitimate_count = sum(1 for email in dataset if email['label'] == 'legitimate')
    
    print(f"\n📊 Statistics:")
    print(f"   Phishing emails: {phishing_count}")
    print(f"   Legitimate emails: {legitimate_count}")
    print(f"   Total: {len(dataset)}")
