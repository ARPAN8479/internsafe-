"""
test_app.py - Automated Tests for InternSafe Backend
===================================================
Tests all endpoints and rule detection heuristics to verify full functionality.
"""

import json
from app import app

def run_tests():
    client = app.test_client()
    passed = 0
    total = 0

    print("--- Running InternSafe Integration Tests ---\n")

    # Test 1: GET / (Analyzer Page)
    total += 1
    resp = client.get('/')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert b"InternSafe" in resp.data, "InternSafe brand missing in index.html"
    assert b"Analyze Offer for Red Flags" in resp.data, "Submit button missing in index.html"
    print("PASS: GET / serves index.html successfully")
    passed += 1

    # Test 2: GET /result (Result Page)
    total += 1
    resp = client.get('/result')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert b"Offer Analysis Result" in resp.data, "Result page title missing"
    assert b"14,800+" not in resp.data, "Fake statistic 14,800+ still present!"
    assert b"14,200+" not in resp.data, "Fake statistic 14,200+ still present!"
    assert b"Over 410 students warned" not in resp.data, "Fake statistic 410 students still present!"
    print("PASS: GET /result serves result.html with fake statistics removed")
    passed += 1

    # Test 3: POST /analyze with empty input
    total += 1
    resp = client.post('/analyze', json={})
    assert resp.status_code == 400, f"Expected 400 for empty input, got {resp.status_code}"
    data = json.loads(resp.data)
    assert "error" in data, "Error message missing in 400 response"
    print("PASS: POST /analyze validates empty input correctly")
    passed += 1

    # Test 4: POST /analyze with realistic Scam Offer
    total += 1
    scam_payload = {
        "offer_text": (
            "Congratulations! Based on your resume shortlist, you are directly selected "
            "for Data Analyst at TechGlobal Innovations Pvt Ltd. Stipend: Rs 35,000 / month. "
            "Work from home 2 hours daily. Kindly pay refundable security deposit of Rs. 1499 "
            "to UPI: hr.onboard@paytm within 6 hours. Send payment screenshot on WhatsApp or "
            "email techglobalsolutions.hr@gmail.com"
        ),
        "company_name": "TechGlobal Innovations Pvt Ltd",
        "sender_email": "techglobalsolutions.hr@gmail.com"
    }
    resp = client.post('/analyze', json=scam_payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = json.loads(resp.data)
    assert "risk_score" in data, "risk_score missing"
    assert "label" in data, "label missing"
    assert "red_flags" in data, "red_flags missing"
    assert data["risk_score"] >= 60, f"Expected high risk score >= 60, got {data['risk_score']}"
    assert data["label"] == "Likely Scam", f"Expected 'Likely Scam', got {data['label']}"
    
    # Verify red flag attributes
    flag_ids = [f["id"] for f in data["red_flags"]]
    assert "REGISTRATION_FEE" in flag_ids, "REGISTRATION_FEE rule should have triggered"
    assert "FREE_EMAIL_DOMAIN" in flag_ids, "FREE_EMAIL_DOMAIN rule should have triggered"
    assert "INSTANT_SELECTION" in flag_ids, "INSTANT_SELECTION rule should have triggered"
    assert "INFORMAL_MESSAGING" in flag_ids, "INFORMAL_MESSAGING rule should have triggered"
    assert "URGENCY_PRESSURE" in flag_ids, "URGENCY_PRESSURE rule should have triggered"

    for flag in data["red_flags"]:
        assert "title" in flag and flag["title"], "Flag missing title"
        assert "explanation" in flag and flag["explanation"], "Flag missing explanation"
        assert "matched_phrase" in flag and flag["matched_phrase"], "Flag missing matched_phrase"

    print(f"PASS: POST /analyze detected Scam Offer with score {data['risk_score']} and {len(data['red_flags'])} red flags")
    passed += 1

    # Test 5: POST /analyze with Safe Offer
    total += 1
    safe_payload = {
        "offer_text": (
            "Dear Rahul, We are pleased to extend an internship offer for Software Engineering "
            "at Infosys Limited following your coding test and technical interview. "
            "Stipend is Rs 15,000 per month. Please sign and return the attached contract from "
            "your university email to admissions@infosys.com within 5 business days."
        ),
        "company_name": "Infosys Limited",
        "sender_email": "admissions@infosys.com"
    }
    resp = client.post('/analyze', json=safe_payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = json.loads(resp.data)
    assert data["risk_score"] < 25, f"Expected low score < 25, got {data['risk_score']}"
    assert data["label"] == "Safe", f"Expected 'Safe', got {data['label']}"
    assert len(data["red_flags"]) == 0, f"Expected 0 red flags, got {len(data['red_flags'])}"
    print(f"PASS: POST /analyze verified Safe Offer with score {data['risk_score']}")
    passed += 1

    # Test 6: POST /analyze with Suspicious Offer (Moderate risk signals)
    total += 1
    suspicious_payload = {
        "offer_text": (
            "Hi, we are conducting a remote social media internship for college students. "
            "Please send your resume to our hiring lead at digitalinterns.india@gmail.com by tomorrow."
        ),
        "company_name": "Digital Trends Media",
        "sender_email": "digitalinterns.india@gmail.com"
    }
    resp = client.post('/analyze', json=suspicious_payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = json.loads(resp.data)
    assert 25 <= data["risk_score"] < 60, f"Expected suspicious score between 25 and 60, got {data['risk_score']}"
    assert data["label"] == "Suspicious", f"Expected 'Suspicious', got {data['label']}"
    print(f"PASS: POST /analyze verified Suspicious Offer with score {data['risk_score']} and label '{data['label']}'")
    passed += 1

    print(f"\n==========================================")
    print(f" ALL {passed}/{total} TESTS PASSED SUCCESSFULLY!")
    print(f"==========================================")

if __name__ == '__main__':
    run_tests()
