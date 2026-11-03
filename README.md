# 🛡️ InternSafe - Fake Internship & Job Offer Detector for Indian Students

**InternSafe** is an educational, beginner-friendly web application designed to protect college students and fresh graduates in India from fraudulent employment rackets, advance-fee scams, and throwaway recruiter identities.

---

## 📌 Project Overview

Every year, thousands of college students fall victim to fake internship offers that demand "refundable security deposits", "training fees", or "laptop courier insurance". InternSafe provides an instant, transparent audit of offer letters, emails, and WhatsApp messages to detect fraud indicators before students pay money or share sensitive documents.

---

## 📂 Project Structure

```
internsafeproject/
│
├── app.py                   # Flask backend server with API & page routes
├── rules.py                 # Rule-based scam detection engine (regex & heuristics)
├── requirements.txt         # Project dependencies (Flask)
├── README.md                # Documentation & run instructions
├── test_app.py              # Automated test suite for endpoints & rules
│
└── frontend/                # Frontend UI (Tailwind CSS + Google Stitch design)
    ├── index.html           # Analyzer page (form, sample loaders, fetch POST)
    └── result.html          # Dynamic results page (SVG gauge, cards, evidence inspector)
```

---

## ⚙️ How the Detection Engine Works (`rules.py`)

The detector implements a **weighted heuristic rule engine** tailored to Indian recruitment schemes:

| # | Rule | Weight | Description |
|---|---|:---:|---|
| **1** | **Registration / Security Fee** | `40` | Checks for keywords like `refundable security deposit`, `training fee`, `processing charge`, `laptop courier`, or UPI payment requests (`@paytm`, `@okaxis`, etc.). *Guarantees minimum score of 65 (Likely Scam).* |
| **2** | **Free Email Domain** | `25` | Detects when supposed corporate recruiters communicate using public handles like `@gmail.com` or `@yahoo.com` instead of authorized company domains (`@company.com`). |
| **3** | **Instant Selection** | `20` | Flags offers claiming immediate selection solely based on CV shortlisting with zero technical screening, coding tests, or interviews. |
| **4** | **WhatsApp / Telegram Contact** | `15` | Flags onboarding and communication conducted exclusively over informal messaging apps without verified portal access. |
| **5** | **Unrealistic Stipend** | `15` | Flags inflated stipends (e.g. ₹35,000 - ₹80,000/mo) for freshers paired with minimal work (2-4 hrs/day flexible data entry or typing). |
| **6** | **Urgency Pressure** | `15` | Detects artificial deadlines ("pay within 6 hours", "seats limited", "offer expires today") designed to prevent consultation with parents or college TPOs. |

### 🎯 Scoring & Classification

- **`0 - 24`**: **Safe** (No known red flags detected; standard corporate patterns).
- **`25 - 59`**: **Suspicious** (Process anomalies, free email, or informal channels; caution advised).
- **`60 - 100`**: **Likely Scam** (High-severity flags like upfront fee demands; do not transfer money).

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python **3.8+** installed on your system.

### 2. Set Up Virtual Environment

Open your terminal or PowerShell inside the project directory:

```bash
# Create a virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt):
.\venv\Scripts\activate.bat

# Activate on macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

You will see:
```
======================================================
 🛡️  InternSafe Backend is running!
 🌐  Analyzer: http://127.0.0.1:5000/
 📊  Results:  http://127.0.0.1:5000/result
======================================================
```

Open **`http://127.0.0.1:5000/`** in your browser to start analyzing offers!

---

## 🧪 Testing

### Automated Test Suite
Run the automated test suite to verify all API routes, rule detections, and UI assertions:

```bash
python test_app.py
```

Expected output:
```
--- Running InternSafe Integration Tests ---
PASS: GET / serves index.html successfully
PASS: GET /result serves result.html with fake statistics removed
PASS: POST /analyze validates empty input correctly
PASS: POST /analyze detected Scam Offer with score 100 and 6 red flags
PASS: POST /analyze verified Safe Offer with score 0
PASS: POST /analyze verified Suspicious Offer with score 25 and label 'Suspicious'
==========================================
 ALL 6/6 TESTS PASSED SUCCESSFULLY!
==========================================
```

### Manual Testing in Browser
The analyzer page (`index.html`) includes 3 one-click sample loader buttons:
1. **🚨 Sample Scam**: Loads an offer demanding a ₹1,499 refundable UPI deposit with a Gmail handle.
2. **⚠️ Sample Suspicious**: Loads a part-time WhatsApp typing offer with unrealistic stipend.
3. **✅ Sample Safe**: Loads an authentic internship offer letter with technical evaluation details and corporate email.

---

## 🔌 API Reference

### `POST /analyze`

Analyzes the offer text and returns structured risk data.

#### Request Body (JSON)
```json
{
  "offer_text": "Dear candidate, you are selected for Data Analyst. Pay Rs. 1499 refundable deposit to hr@paytm within 6 hours. Contact hr.desk@gmail.com",
  "company_name": "TechGlobal Solutions Pvt Ltd",
  "sender_email": "hr.desk@gmail.com"
}
```

#### Response Body (JSON)
```json
{
  "risk_score": 100,
  "label": "Likely Scam",
  "summary": "Multiple high-severity red flags detected typical of fee-for-offer scams targeting college graduates across India.",
  "company_name": "TechGlobal Solutions Pvt Ltd",
  "sender_email": "hr.desk@gmail.com",
  "metrics": {
    "stipend": "Not Specified",
    "fee": "₹1,499 (UPI / Deposit)",
    "recruiter_origin": "Personal Gmail"
  },
  "red_flags": [
    {
      "id": "REGISTRATION_FEE",
      "title": "Demands Upfront Registration or Security Fee",
      "severity": "high",
      "weight": 40,
      "matched_phrase": "...selected for Data Analyst. Pay Rs. 1499 refundable deposit to hr@paytm within 6 hours...",
      "explanation": "Legitimate Indian corporations never charge candidates application fees or security deposits..."
    },
    {
      "id": "FREE_EMAIL_DOMAIN",
      "title": "Recruiter Uses Free Public Email (@gmail / @yahoo)",
      "severity": "high",
      "weight": 25,
      "matched_phrase": "hr.desk@gmail.com",
      "explanation": "Authorized corporate recruiters communicate strictly through authenticated company domains..."
    }
  ]
}
```

---

## 🎓 Student Safety Guidelines

1. **Zero Registration Fee Policy**: Under Ministry of Labour and Employment guidelines, no authentic recruiter charges candidates for interviews, ID badges, background checks, or laptop dispatch.
2. **Ministry of Corporate Affairs (MCA)**: Verify company registration and CIN numbers on [mca.gov.in](https://www.mca.gov.in).
3. **National Cyber Crime Helpline**: If you were scammed, dial **1930** or register a complaint at [cybercrime.gov.in](https://cybercrime.gov.in).
