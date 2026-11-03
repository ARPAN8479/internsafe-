<div align="center">

# 🛡️ InternSafe

### Fake Internship & Job Offer Detector for Indian Students

Paste a suspicious offer message. Get an instant risk score and a clear, explainable list of red flags.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-Frontend-06B6D4?logo=tailwindcss&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-6%2F6_passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## 📸 Screenshots

| Analyzer | Result |
|---|---|
| ![Analyzer page](docs/screenshot-analyzer.png) | ![Result page](docs/screenshot-result.png) |

> 💡 Add your screenshots to a `docs/` folder with the file names above.

---

## 📌 The Problem

Every year, many students in India lose money to fake internship offers that ask for a "refundable security deposit", "training fee", or "laptop courier insurance". These messages usually arrive on WhatsApp, Telegram, or email, and they rely on urgency and a lack of verification.

## 💡 The Solution

**InternSafe** analyzes an offer message and explains *why* it looks safe or risky, rather than just returning a label. Each result includes:

- A **risk score (0-100)** and a label: *Safe*, *Suspicious*, or *Likely Scam*
- **Red-flag cards** with a severity level, explanation, and the exact phrase that triggered the flag
- **Extracted details**: fee mentioned, stipend, and the recruiter's email type
- **Safety guidance** on what to do next

> ⚠️ **Disclaimer:** InternSafe is an educational project. It is a screening aid, not a guarantee. Always verify companies independently before sharing money or documents.

---

## ✨ Features

- ⚖️ Weighted, rule-based detection tuned to common scam patterns in India
- 🔍 Explainable results: every flag shows what matched and why it matters
- 🧪 One-click sample loaders (scam, suspicious, safe) for quick demos
- 📊 Dynamic results page with an SVG risk gauge and an evidence inspector
- ✅ Automated test suite for routes and detection rules
- 🎨 Responsive UI designed in Google Stitch and built with Tailwind CSS

---

## 🧠 How Detection Works

InternSafe uses a weighted heuristic engine implemented in [`rules.py`](rules.py). Each rule that fires adds its weight to the risk score (capped at 100).

| # | Rule | Weight | What it looks for |
|---|---|:---:|---|
| 1 | Registration / Security Fee | 40 | Terms such as refundable deposit, training fee, processing charge, laptop courier, or UPI payment requests. Sets a minimum score of 65 (*Likely Scam*). |
| 2 | Free Email Domain | 25 | A "company recruiter" using `@gmail.com`, `@yahoo.com`, or similar instead of a company domain. |
| 3 | Instant Selection | 20 | Selection based only on a CV, with no interview, test, or technical screening. |
| 4 | WhatsApp / Telegram Contact | 15 | Onboarding done only over informal messaging apps. |
| 5 | Unrealistic Stipend | 15 | Very high pay for freshers paired with minimal work, such as simple typing or data entry. |
| 6 | Urgency Pressure | 15 | Artificial deadlines such as "pay within 6 hours" or "offer expires today". |

### Score Classification

| Score | Label | Meaning |
|:---:|---|---|
| 0 - 24 | 🟢 **Safe** | No known red flags detected. |
| 25 - 59 | 🟠 **Suspicious** | Process anomalies found. Verify before proceeding. |
| 60 - 100 | 🔴 **Likely Scam** | High-severity flags such as an upfront fee demand. Do not transfer money. |

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Detection | Regex and weighted heuristics |
| Frontend | HTML, Tailwind CSS (designed in Google Stitch) |
| Testing | Python test script (`test_app.py`) |

---

## 📂 Project Structure

```
internsafe/
├── app.py              # Flask server: page routes and /analyze API
├── rules.py            # Rule-based scam detection engine
├── requirements.txt    # Dependencies
├── test_app.py         # Automated tests for routes and rules
├── README.md
└── frontend/
    ├── index.html      # Analyzer page (form, sample loaders, fetch POST)
    └── result.html     # Results page (SVG gauge, flag cards, evidence inspector)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/internsafe.git
cd internsafe
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

Then open **http://127.0.0.1:5000/** in your browser.

---

## 🧪 Testing

Run the automated suite:

```bash
python test_app.py
```

Expected output:

```
PASS: GET / serves index.html successfully
PASS: GET /result serves result.html with fake statistics removed
PASS: POST /analyze validates empty input correctly
PASS: POST /analyze detected Scam Offer with score 100 and 6 red flags
PASS: POST /analyze verified Safe Offer with score 0
PASS: POST /analyze verified Suspicious Offer with score 25 and label 'Suspicious'
ALL 6/6 TESTS PASSED SUCCESSFULLY!
```

### Manual testing
The analyzer page has three sample buttons:

- 🚨 **Sample Scam:** a ₹1,499 refundable UPI deposit request from a Gmail address
- ⚠️ **Sample Suspicious:** a part-time WhatsApp typing job with an unrealistic stipend
- ✅ **Sample Safe:** a genuine-style offer with a technical evaluation and corporate email

### Evaluation on sample messages

I also tested the tool on 10 hand-written messages (5 scam-style, 5 genuine-style).

| Result | Count |
|---|:---:|
| Scam messages correctly flagged | _X / 5_ |
| Genuine messages correctly marked safe | _X / 5_ |
| False alarms | _X_ |

> 📝 Replace the `X` values with your own results. Small, hand-made samples show how the rules behave, not real-world accuracy.

---

## 🔌 API Reference

### `POST /analyze`

Analyzes offer text and returns structured risk data.

**Request**
```json
{
  "offer_text": "Dear candidate, you are selected for Data Analyst. Pay Rs. 1499 refundable deposit to hr@paytm within 6 hours. Contact hr.desk@gmail.com",
  "company_name": "TechGlobal Solutions Pvt Ltd",
  "sender_email": "hr.desk@gmail.com"
}
```

`offer_text` is required. `company_name` and `sender_email` are optional.

**Response**
```json
{
  "risk_score": 100,
  "label": "Likely Scam",
  "summary": "Multiple high-severity red flags detected typical of fee-for-offer scams.",
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
      "matched_phrase": "...Pay Rs. 1499 refundable deposit to hr@paytm within 6 hours...",
      "explanation": "Legitimate companies do not charge candidates fees to hire them."
    }
  ]
}
```

---

## ⚠️ Limitations

Being upfront about what this project does *not* do:

- **Rule-based, not machine learning.** It matches known patterns, so new or cleverly worded scams can slip through.
- **Keyword and regex matching** can produce false positives and false negatives.
- **English-focused.** Messages in Hindi or Hinglish may not be detected well.
- **No live verification.** It does not check company registration, domain age, or phone numbers online.
- **Evaluated on a small sample set**, so accuracy claims should not be generalized.

## 🛣️ Roadmap

- [ ] Train a text classifier (TF-IDF + Logistic Regression) on a labeled dataset and combine it with the rules
- [ ] Add Hindi and Hinglish keyword support
- [ ] Check email domain age and basic URL reputation
- [ ] Add a "Scam Tips" education page
- [ ] Deploy a public demo (Render or Hugging Face Spaces)

---

## 🎓 Student Safety Tips

- **Real recruiters do not ask you to pay** for interviews, ID cards, training kits, or laptop shipping.
- **Verify the company:** check its official website and LinkedIn page, and look up registered companies on [mca.gov.in](https://www.mca.gov.in).
- **Check the sender's email domain.** Be careful if a "company" uses Gmail or Yahoo.
- **Talk to your college placement cell (TPO)** before accepting offers you are unsure about.
- **If you were scammed:** call **1930** (National Cyber Crime Helpline) or file a complaint at [cybercrime.gov.in](https://cybercrime.gov.in). Contact your bank quickly as well.

---

## 👤 Author

**Arpan**
B.Tech CSE (AI & ML), SGT University

- GitHub: [@YOUR-USERNAME](https://github.com/YOUR-USERNAME)
- LinkedIn: [your-profile](https://www.linkedin.com/in/YOUR-PROFILE)

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

<div align="center">

If this project helped you, consider giving it a ⭐

</div>
