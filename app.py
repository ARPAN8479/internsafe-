"""
app.py - InternSafe Backend Server
===================================
A beginner-friendly Flask application designed to protect Indian college students
from fake job offers and internship fraud syndicates.

Routes:
  - GET  /         : Serves the Analyzer Page (index.html)
  - GET  /result   : Serves the Analysis Result Page (result.html)
  - POST /analyze  : Receives offer text & metadata, runs the rule engine,
                     and returns JSON containing risk score, label, and red flags.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from rules import analyze_offer

# Initialize the Flask application
# We point static_folder to 'frontend' so static HTML/CSS/JS files are served directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')


# ==============================================================================
# FRONTEND PAGE ROUTES
# ==============================================================================

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main analyzer page (index.html) where students can paste
    their job/internship offer letter, email, or WhatsApp message.
    """
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/result', methods=['GET'])
def result():
    """
    Renders the result page (result.html) where verification metrics,
    the risk score meter, and red-flag evidence cards are displayed.
    """
    return send_from_directory(FRONTEND_DIR, 'result.html')


# ==============================================================================
# API ANALYSIS ROUTE
# ==============================================================================

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    POST /analyze
    ----------------
    Accepts JSON (or form-encoded) input containing:
      - offer_text    (string, required): The body of the offer email or message
      - company_name  (string, optional): Claimed company or employer name
      - sender_email  (string, optional): Email or contact address of the sender

    Returns JSON:
      {
        "risk_score": 0 - 100,
        "label": "Safe" | "Suspicious" | "Likely Scam",
        "red_flags": [
          {
            "id": "REGISTRATION_FEE",
            "title": "...",
            "severity": "high",
            "matched_phrase": "...",
            "explanation": "..."
          },
          ...
        ],
        "metrics": {
          "stipend": "₹35,000 / mo",
          "fee": "₹1,499 (UPI)",
          "recruiter_origin": "Personal Gmail"
        },
        "summary": "...",
        "company_name": "...",
        "sender_email": "...",
        "original_text": "..."
      }
    """
    # 1. Parse incoming request data (supports both JSON and HTML form submissions)
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    offer_text = data.get('offer_text') or data.get('text', '')
    company_name = data.get('company_name', '')
    sender_email = data.get('sender_email', '')

    # 2. Validate input
    if not offer_text or not offer_text.strip():
        return jsonify({
            "error": "Please provide the internship or job offer text to analyze."
        }), 400

    # 3. Execute the rule-based detection engine (from rules.py)
    analysis_result = analyze_offer(
        offer_text=offer_text,
        company_name=company_name,
        sender_email=sender_email
    )

    # 4. Attach original text for the front-end evidence auditor
    analysis_result['original_text'] = offer_text

    # 5. Return structured JSON response
    return jsonify(analysis_result), 200


# ==============================================================================
# RUN SERVER (LOCAL DEVELOPMENT)
# ==============================================================================

if __name__ == '__main__':
    import sys
    # Avoid UnicodeEncodeError on Windows consoles with cp1252/ascii
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    # Run development server on port 5000 with debug enabled for easy learning
    print("======================================================")
    print(" [*] InternSafe Backend is running!")
    print(" [*] Analyzer: http://127.0.0.1:5000/")
    print(" [*] Results:  http://127.0.0.1:5000/result")
    print("======================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
