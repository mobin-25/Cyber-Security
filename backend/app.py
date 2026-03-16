import json
import os
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app) 

# Initialize the NEW Google GenAI Client
# It automatically looks for GEMINI_API_KEY in your .env file
client = genai.Client()

# --- 1. SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are a cybersecurity expert specializing in phone scam and phishing detection in Indian regional languages.

Analyze the given message/transcript and return ONLY valid JSON (no extra text) in this exact format:
{
  "risk_level": "SAFE" | "SUSPICIOUS" | "HIGH",
  "score": <number 0-100>,
  "language_detected": "Hindi/Marathi/Tamil/English",
  "flagged_phrases": [
    {"text": "...", "reason": "..."}
  ],
  "tactics": ["urgency","otp_request","authority_claim","fear","reward_offer","personal_info_request"],
  "summary": "One sentence explanation in English"
}

Scam indicators to detect:
- OTP / password requests
- Urgent payment demands (अभी करें, तुरंत)
- Fake authority (RBI, bank, police, court)
- Threats (account block, arrest, fine)
- Too-good offers (lottery, prize, job)
- Personal info requests (Aadhaar, PAN, account no.)
"""

# --- 2. RULE-BASED FALLBACK ---
SCAM_KEYWORDS = {
  "hi": ["OTP", "खाता बंद", "तुरंत", "पुरस्कार", "RBI", "पुलिस", "फर्जी"],
  "mr": ["OTP", "खाते बंद", "लगेच", "बक्षीस"],
  "ta": ["OTP", "கணக்கு", "உடனே", "பரிசு"]
}

def keyword_score(text, lang):
    keywords = SCAM_KEYWORDS.get(lang, [])
    hits = sum(1 for k in keywords if k in text)
    return min(hits * 20, 80)

# --- 3. THE MAIN API ENDPOINT ---
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data.get('text')   
    lang = data.get('lang', 'auto')

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this message (language: {lang}):\n\n{text}"
        
        # Use the NEW SDK syntax with the latest fast model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        # Clean the response just in case Gemini wraps it in markdown
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        return jsonify(result)

    except Exception as e:
        print(f"AI API Failed: {e}")
        fallback_score = keyword_score(text, lang)
        fallback_risk = "HIGH" if fallback_score > 60 else "SUSPICIOUS" if fallback_score > 0 else "SAFE"
        
        return jsonify({
            "risk_level": fallback_risk,
            "score": fallback_score,
            "language_detected": lang,
            "flagged_phrases": [{"text": "API Error", "reason": "Used fallback keyword detection"}],
            "tactics": ["system_fallback"],
            "summary": "AI analysis failed. Evaluated using keyword fallback."
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)