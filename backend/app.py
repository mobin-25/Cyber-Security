import json
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
from detector import detect_scam

# Load environment variables (optional now since key is hardcoded for demo)
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Hardcoded for demo stability to avoid .env visibility issues
API_KEY = "AIzaSyDe90DUkG7ZA6Vmf8ReCvGERW8mQidpLk"
client = genai.Client(api_key=API_KEY)

# --- 1. AUDIO TRANSCRIPTION ENDPOINT (Member 2) ---
@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    temp_path = f"temp_{audio_file.filename}"
    
    try:
        audio_file.save(temp_path)
        uploaded_file = client.files.upload(path=temp_path)

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(1)
            uploaded_file = client.files.get(name=uploaded_file.name)

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[uploaded_file, "Transcribe this audio exactly into the text spoken."]
        )

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
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Analyze this scam text and return ONLY JSON: {text}"
        )
        
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