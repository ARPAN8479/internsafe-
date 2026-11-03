"""
rules.py - Rule-Based Detection Engine for InternSafe
=====================================================
This module evaluates internship and job offer communications directed at Indian students.
It uses pattern matching (regular expressions) and weighted heuristics to identify common
fraud signatures, such as upfront security fees, throwaway email domains, informal messaging,
unrealistic stipends, instant hiring without interviews, and artificial urgency.
"""

import re
from typing import Dict, List, Any, Optional


# ==============================================================================
# RULE DEFINITIONS & WEIGHTS
# ==============================================================================
# Each rule represents a well-known tactic used by employment scammers in India.
# Weights determine how heavily each triggered rule contributes to the total risk score (0-100).

RULE_WEIGHTS = {
    "REGISTRATION_FEE": 40,      # Demanding money upfront is the #1 scam indicator in India
    "FREE_EMAIL_DOMAIN": 25,     # Official HR never uses personal gmail/yahoo for corporate hiring
    "INSTANT_SELECTION": 20,     # Hiring with zero technical evaluation or interview is a huge anomaly
    "INFORMAL_MESSAGING": 15,    # Solely relying on WhatsApp/Telegram instead of official enterprise channels
    "UNREALISTIC_STIPEND": 15,   # Absurdly high pay for freshers/minimal part-time work (bait hook)
    "URGENCY_PRESSURE": 15,      # False deadlines ("pay within 6 hrs") to force rash decisions
}

# Free public email providers commonly abused by fake recruiters
FREE_EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "yahoo.co.in",
    "rediffmail.com",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "icloud.com",
    "protonmail.com"
]


# ==============================================================================
# HELPER EXTRACTION FUNCTIONS
# ==============================================================================

def find_matched_snippet(pattern: re.Pattern, text: str, max_length: int = 120) -> Optional[str]:
    """
    Search for a regex match in the text and return a clean, user-readable snippet
    centered around the match to serve as evidence in the audit report.
    """
    match = pattern.search(text)
    if not match:
        return None

    # Get start and end indices of the match
    start, end = match.span()

    # Expand slightly to capture surrounding sentence context
    context_start = max(0, start - 20)
    context_end = min(len(text), end + 40)

    snippet = text[context_start:context_end].strip()

    # Clean up multi-line formatting in snippet
    snippet = re.sub(r'\s+', ' ', snippet)

    if context_start > 0:
        snippet = "..." + snippet
    if context_end < len(text):
        snippet = snippet + "..."

    return snippet


# ==============================================================================
# INDIVIDUAL RULE CHECKERS
# ==============================================================================

def check_registration_fee(text: str) -> Optional[Dict[str, Any]]:
    """
    RULE 1: Checks for registration fees, refundable deposits, processing charges,
    or UPI payment requests. Legitimate Indian employers never charge candidates.
    """
    # Regex 1: Explicit fee/deposit keywords (e.g. "refundable security deposit", "registration fee")
    fee_keywords_pattern = re.compile(
        r'\b(registration|security|processing|caution|training|onboarding|verification|laptop|courier|gate\s*pass|document)\s+'
        r'(?:fee|deposit|charge|charges|amount|cost|money)\b',
        re.IGNORECASE
    )

    # Regex 2: Mention of UPI / Payment gateways with money actions
    payment_action_pattern = re.compile(
        r'\b(pay|transfer|deposit|send|scan|qr\s*code|bhim|upi|paytm|phonepe|gpay|google\s*pay)\b.*?'
        r'(?:(?:rs\.?|inr|₹)\s*\d+|\d+\s*(?:rs|inr|rupees))',
        re.IGNORECASE
    )

    # Regex 3: Refundable fee promises (classic trap: "pay 1500, refunded in first salary")
    refundable_trap_pattern = re.compile(
        r'\b(refundable\s+(?:fee|deposit|amount|security)|refunded\s+(?:in|with|after)\s+(?:1st|first)\s+(?:month|salary))\b',
        re.IGNORECASE
    )

    # Regex 4: UPI ID handles (e.g. hr.onboard@paytm, company@okaxis)
    upi_handle_pattern = re.compile(
        r'\b[a-zA-Z0-9.\-_]{2,}@(paytm|okaxis|okhdfcbank|oksbi|icici|ybl|axl|upi|postbank|ibl)\b',
        re.IGNORECASE
    )

    matched_snippet = None

    for pattern in [refundable_trap_pattern, fee_keywords_pattern, payment_action_pattern, upi_handle_pattern]:
        snippet = find_matched_snippet(pattern, text)
        if snippet:
            matched_snippet = snippet
            break

    if matched_snippet:
        return {
            "id": "REGISTRATION_FEE",
            "title": "Demands Upfront Registration or Security Fee",
            "severity": "high",
            "weight": RULE_WEIGHTS["REGISTRATION_FEE"],
            "matched_phrase": matched_snippet,
            "explanation": (
                "Legitimate Indian corporations and registered startups never ask candidates "
                "to pay application charges, training fees, laptop courier deposits, or gate pass fees. "
                "Any request to send money—even if claimed to be '100% refundable'—is a confirmed indicator of job fraud."
            )
        }
    return None


def check_free_email_domain(text: str, sender_email: Optional[str] = None, company_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    RULE 2: Checks if official corporate communication uses a free public email
    provider (like @gmail.com or @yahoo.com) rather than an official corporate domain.
    """
    detected_email = None

    # First inspect explicit sender email passed by user
    if sender_email:
        sender_email_clean = sender_email.strip().lower()
        for domain in FREE_EMAIL_DOMAINS:
            if sender_email_clean.endswith("@" + domain):
                detected_email = sender_email.strip()
                break

    # If not found yet, scan the text body for email addresses
    if not detected_email:
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b')
        for match in email_pattern.finditer(text):
            found_email = match.group(0)
            domain = match.group(1).lower()
            if domain in FREE_EMAIL_DOMAINS:
                detected_email = found_email
                break

    if detected_email:
        company_ref = f"claiming to represent '{company_name}'" if company_name else "claiming to be an official recruiter"
        return {
            "id": "FREE_EMAIL_DOMAIN",
            "title": "Recruiter Uses Free Public Email (@gmail / @yahoo)",
            "severity": "high",
            "weight": RULE_WEIGHTS["FREE_EMAIL_DOMAIN"],
            "matched_phrase": detected_email,
            "explanation": (
                f"The sender {company_ref} uses a free public email address ({detected_email}). "
                "Authorized corporate recruiters in India communicate strictly through authenticated "
                "company domains (e.g. name@tcs.com or careers@startup.in) to comply with data security and compliance."
            )
        }
    return None


def check_instant_selection(text: str) -> Optional[Dict[str, Any]]:
    """
    RULE 3: Checks for guaranteed appointment letters issued without technical screening,
    interviews, or formal skill assessments.
    """
    selection_pattern = re.compile(
        r'\b(directly\s+selected|direct\s+selection|direct\s+hiring|selected\s+directly|'
        r'instant\s+selection|no\s+interview\s*(?:required|needed|conducted)?|'
        r'selected\s+without\s+interview|without\s+any\s+interview|'
        r'guaranteed\s+(?:selection|job|internship|appointment|placement)|'
        r'selected\s+based\s+on\s+(?:your\s+)?(?:resume|cv|profile)\s*(?:shortlist|review)?|'
        r'zero\s+(?:technical\s+)?screening)\b',
        re.IGNORECASE
    )

    matched_snippet = find_matched_snippet(selection_pattern, text)
    if matched_snippet:
        return {
            "id": "INSTANT_SELECTION",
            "title": "Instant Selection Without Any Interview",
            "severity": "medium",
            "weight": RULE_WEIGHTS["INSTANT_SELECTION"],
            "matched_phrase": matched_snippet,
            "explanation": (
                "Real companies evaluate student skills through coding tests, technical interviews, "
                "or HR discussions. Direct offer letters issued solely upon CV upload correlate over 85% "
                "with fee-charging syndicates that target eager students."
            )
        }
    return None


def check_informal_messaging(text: str) -> Optional[Dict[str, Any]]:
    """
    RULE 4: Checks if the recruitment, onboarding, or payment verification is driven
    exclusively through informal platforms like WhatsApp or Telegram.
    """
    messaging_pattern = re.compile(
        r'\b(?:via|on|through|over|contact|message|dm|chat|send|forward|screenshot\s+on)?\s*'
        r'(?:whatsapp|telegram)\b|'
        r'\b(?:wa\.me|t\.me|chat\.whatsapp\.com)\b',
        re.IGNORECASE
    )

    matched_snippet = find_matched_snippet(messaging_pattern, text)
    if matched_snippet:
        return {
            "id": "INFORMAL_MESSAGING",
            "title": "Recruitment Conducted Exclusively via WhatsApp / Telegram",
            "severity": "medium",
            "weight": RULE_WEIGHTS["INFORMAL_MESSAGING"],
            "matched_phrase": matched_snippet,
            "explanation": (
                "While preliminary contact can happen anywhere, legitimate enterprise onboarding "
                "occurs via official HR portals, encrypted applicant tracking systems, and official email. "
                "Handling job offers, UPI transactions, and identity proofs exclusively over WhatsApp/Telegram "
                "is standard scam tradecraft to avoid corporate oversight."
            )
        }
    return None


def check_unrealistic_stipend(text: str) -> Optional[Dict[str, Any]]:
    """
    RULE 5: Checks for suspiciously inflated compensation offered for entry-level,
    intern, or minimal part-time roles (e.g. ₹35,000 - ₹80,000/month for 2 hrs/day).
    """
    # Look for high monetary figures linked to monthly stipends
    stipend_pattern = re.compile(
        r'(?:rs\.?|inr|₹)\s*([3-9]\d|\d{3,})\s*(?:,|k|thousand)?\s*(?:\/|\s*per\s*)?\s*(?:month|mo|pm)\b',
        re.IGNORECASE
    )

    # Low-effort buzzwords that scammers bundle with high pay
    low_effort_pattern = re.compile(
        r'\b(part[\s-]*time|flexible\s*(?:hours|timings)|[1-4]\s*(?:hrs?|hours?)\s*(?:\/|\s*per\s*)?\s*day|'
        r'no\s*experience|data\s*entry|typing\s*work|form\s*filling|work\s*from\s*home)\b',
        re.IGNORECASE
    )

    stipend_match = stipend_pattern.search(text)
    low_effort_match = low_effort_pattern.search(text)

    # Trigger if high stipend is detected (especially if combined with low-effort buzzwords)
    if stipend_match:
        matched_snippet = find_matched_snippet(stipend_pattern, text)
        return {
            "id": "UNREALISTIC_STIPEND",
            "title": "Unrealistically High Stipend for Freshers / Minimal Effort",
            "severity": "medium",
            "weight": RULE_WEIGHTS["UNREALISTIC_STIPEND"],
            "matched_phrase": matched_snippet,
            "explanation": (
                "Average Indian student internships typically offer ₹5,000 to ₹18,000/month for skilled engineering/business roles. "
                "Promising ₹30,000 to ₹80,000+ per month for flexible 2-4 hours/day or entry-level tasks is classic bait "
                "to make candidates overlook subsequent fee requests."
            )
        }
    elif low_effort_match and re.search(r'(?:rs\.?|inr|₹)\s*\d+', text, re.IGNORECASE):
        # Even without explicit monthly tag, low effort + money
        matched_snippet = find_matched_snippet(low_effort_pattern, text)
        return {
            "id": "UNREALISTIC_STIPEND",
            "title": "Low Effort / High Pay Promise Anomaly",
            "severity": "low",
            "weight": 10,
            "matched_phrase": matched_snippet,
            "explanation": (
                "The offer promises attractive compensation for minimal hours or vague remote work. "
                "Always verify whether the role includes tangible technical deliverables."
            )
        }
    return None


def check_urgency_pressure(text: str) -> Optional[Dict[str, Any]]:
    """
    RULE 6: Checks for artificial time pressure designed to prevent students
    from consulting their college TPO, parents, or verifying company credentials.
    """
    urgency_pattern = re.compile(
        r'\b(?:within|in)\s+(\d{1,2}|few)\s*(?:hours?|hrs?|minutes?|mins?)\b|'
        r'\b(offer\s+(?:expires?|valid)\s*(?:today|tonight|within)|'
        r'last\s+date\s*(?:today|tomorrow)|urgent\s+(?:joining|hiring|requirement)|'
        r'seats?\s+(?:are\s+)?limited|only\s+\d+\s+slots?\s+left|'
        r'act\s+immediately|immediate\s+confirmation\s+required|hurry\s+up)\b',
        re.IGNORECASE
    )

    matched_snippet = find_matched_snippet(urgency_pattern, text)
    if matched_snippet:
        return {
            "id": "URGENCY_PRESSURE",
            "title": "High-Pressure Urgency Tactics",
            "severity": "low",
            "weight": RULE_WEIGHTS["URGENCY_PRESSURE"],
            "matched_phrase": matched_snippet,
            "explanation": (
                "Scammers use tight artificial deadlines (e.g. 'pay within 6 hours' or 'seats limited') "
                "to induce panic. Genuine Indian corporate hiring processes grant candidates several days "
                "to review and sign formal contracts."
            )
        }
    return None


# ==============================================================================
# KEY METRIC EXTRACTORS (FOR UI CARDS)
# ==============================================================================

def extract_key_metrics(text: str, sender_email: Optional[str] = None) -> Dict[str, str]:
    """
    Extracts high-level summary metrics (stipend, fee, origin) to display
    in the result overview cards.
    """
    # 1. Stipend Claimed:
    # Requires explicit monthly tag (e.g. ₹35,000 / month, ₹15000 pm) or explicit stipend/salary keyword
    stipend_match = re.search(
        r'(?:stipend|salary|package|pay|compensation)?\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)\s*([\d,]+)\s*(?:\/|\s*per\s*)?\s*(?:month|mo|pm)\b',
        text, re.IGNORECASE
    )
    if not stipend_match:
        stipend_match = re.search(
            r'\b(?:stipend|salary)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)\s*([\d,]+)\b',
            text, re.IGNORECASE
        )
    stipend_val = f"₹{stipend_match.group(1)} / mo" if stipend_match else "Not Specified"

    # 2. Requested Deposit / Fee:
    # Looks for amounts specifically tied to fee/deposit/charge/UPI keywords
    fee_match = re.search(
        r'(?:fee|deposit|charge|charges|amount|pay|transfer|upi|paytm|refundable)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)\s*(\d+[\d,]*)',
        text, re.IGNORECASE
    )
    if not fee_match:
        fee_match = re.search(
            r'(?:rs\.?|inr|₹)\s*(\d+[\d,]*)\s*(?:for|as|towards)?\s*(?:fee|deposit|charge|processing|verification|registration)',
            text, re.IGNORECASE
        )

    has_fee_context = re.search(r'\b(fee|deposit|charge|upi|paytm|phonepe|gpay|refundable)\b', text, re.IGNORECASE)
    
    if fee_match:
        fee_val = f"₹{fee_match.group(1)} (UPI / Deposit)"
    elif has_fee_context:
        fee_val = "Fee Demanded (UPI)"
    else:
        fee_val = "None Detected"

    # 3. Recruiter Origin / Domain
    detected_email = sender_email or ""
    if not detected_email:
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', text)
        if email_match:
            detected_email = email_match.group(0)

    if detected_email:
        domain = detected_email.split('@')[-1].lower()
        if domain in FREE_EMAIL_DOMAINS:
            origin_val = f"Personal {domain.split('.')[0].capitalize()}"
        else:
            origin_val = f"Corporate (@{domain})"
    elif re.search(r'\b(whatsapp|telegram)\b', text, re.IGNORECASE):
        origin_val = "Messaging Forward"
    else:
        origin_val = "Unverified Domain"

    return {
        "stipend": stipend_val,
        "fee": fee_val,
        "recruiter_origin": origin_val
    }


# ==============================================================================
# MAIN ANALYZER ORCHESTRATOR
# ==============================================================================

def analyze_offer(offer_text: str, company_name: Optional[str] = None, sender_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point for offer analysis.
    Executes all rule checkers, computes total risk score, determines safety label,
    and formats red flags.
    
    Returns a dictionary ready for JSON serialization:
    {
        "risk_score": int (0-100),
        "label": "Safe" | "Suspicious" | "Likely Scam",
        "red_flags": [...],
        "metrics": {...},
        "summary": str,
        "company_name": str,
        "sender_email": str
    }
    """
    if not offer_text or not offer_text.strip():
        return {
            "risk_score": 0,
            "label": "Safe",
            "red_flags": [],
            "metrics": {"stipend": "N/A", "fee": "None", "recruiter_origin": "N/A"},
            "summary": "No text provided for analysis.",
            "company_name": company_name or "Unknown Company",
            "sender_email": sender_email or "Not Provided"
        }

    red_flags: List[Dict[str, Any]] = []

    # Run all 6 rule checks
    rule_results = [
        check_registration_fee(offer_text),
        check_free_email_domain(offer_text, sender_email=sender_email, company_name=company_name),
        check_instant_selection(offer_text),
        check_informal_messaging(offer_text),
        check_unrealistic_stipend(offer_text),
        check_urgency_pressure(offer_text),
    ]

    # Collect matched flags
    raw_score = 0
    has_critical_fee = False

    for flag in rule_results:
        if flag:
            red_flags.append(flag)
            raw_score += flag.get("weight", 0)
            if flag.get("id") == "REGISTRATION_FEE":
                has_critical_fee = True

    # If an upfront fee is demanded, this is an instant scam signal in India.
    # We guarantee a minimum score of 65 (Likely Scam).
    if has_critical_fee and raw_score < 65:
        raw_score = 65

    # If multiple high-severity flags triggered (e.g. fee + free email domain),
    # boost score to reflect compounded risk
    if has_critical_fee and len(red_flags) >= 2:
        raw_score = max(raw_score, 85)

    # Clamp score strictly between 0 and 100
    risk_score = max(0, min(100, raw_score))

    # Assign risk classification label based on the composite score
    if risk_score >= 60:
        label = "Likely Scam"
        summary = (
            "Multiple high-severity red flags detected typical of fee-for-offer scams "
            "targeting college graduates across India. Do not transfer any funds or share identity documents."
        )
    elif risk_score >= 25:
        label = "Suspicious"
        summary = (
            "Process anomalies or informal communication channels detected. Exercise caution and verify "
            "the employer's corporate identity independently before proceeding."
        )
    else:
        label = "Safe"
        summary = (
            "No common fraudulent patterns or fee requests detected. Maintain standard precautions "
            "and ensure any official offer letter comes from an authenticated company domain."
        )

    # Extract UI metrics
    metrics = extract_key_metrics(offer_text, sender_email=sender_email)

    # Try extracting company name from text if not provided
    effective_company = company_name.strip() if (company_name and company_name.strip()) else None
    if not effective_company:
        # Search for company markers like "Pvt Ltd", "Private Limited", "Technologies", "Solutions"
        company_match = re.search(r'\b([A-Z][A-Za-z0-9\s&]{2,30}(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|LLP|Technologies|Solutions|Innovations|Infotech))\b', offer_text)
        if company_match:
            effective_company = company_match.group(1).strip()
        else:
            effective_company = "Unverified Entity / Company"

    return {
        "risk_score": risk_score,
        "label": label,
        "summary": summary,
        "red_flags": red_flags,
        "metrics": metrics,
        "company_name": effective_company,
        "sender_email": sender_email.strip() if sender_email else ""
    }
