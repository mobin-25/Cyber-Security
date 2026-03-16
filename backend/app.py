from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import detect_scam

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.json["text"]

    risk, detected = detect_scam(text)

    return jsonify({
        "risk": risk,
        "detected": detected
    })

if __name__ == "__main__":
    app.run(debug=True)