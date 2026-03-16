import json
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
from detector import detect_scam

# Load environment variables (optional now since key is hardcoded for demo)
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Hardcoded for demo stability to avoid .env visibility issues
API_KEY = "AIzaSyDe90DUkG7ZA6Vmf8ReCvGERW8mQidpLk"
genai.configure(api_key=API_KEY)

# --- 1. AUDIO TRANSCRIPTION ENDPOINT (Member 2) ---
@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    temp_path = f"temp_{audio_file.filename}"
    
    try:
        audio_file.save(temp_path)
        uploaded_file = genai.upload_file(path=temp_path)

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(1)
            uploaded_file = genai.get_file(name=uploaded_file.name)

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([uploaded_file, "Transcribe this audio exactly into the text spoken."])

        os.remove(temp_path)
        return jsonify({"transcript": response.text})

    except Exception as e:
        print(f"Transcription Error: {e}")
        if os.path.exists(temp_path): os.remove(temp_path)
        return jsonify({"transcript": "Could not transcribe audio. (Demo Fallback)"})

# --- 2. AI ANALYSIS ENDPOINT (Member 3) ---
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')

    try:
        # Try the live Gemini AI first
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"Analyze this scam text and return ONLY JSON: {text}")
        
        # Parse the AI response
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return jsonify(json.loads(clean_text))

    except Exception as e:
        # 🚨 FALLBACK 1: Use built-in keyword detector 🚨
        print(f"AI API Failed or Limit Hit: {e}. Using Keyword Detector Fallback.")
        
        risk, detected = detect_scam(text)
        
        return jsonify({
            "risk": risk,
            "detected": detected,
            "method": "keyword_detection"
        })

if __name__ == '__main__':
    # Running on http://127.0.0.1:5000
    app.run(debug=True, port=5000)