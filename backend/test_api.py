import requests
import json

url = "http://127.0.0.1:5000/api/analyze"

# We are sending a high-risk Hindi scam message to test it
data = {
    "text": "आपका SBI खाता बंद हो जाएगा। अभी OTP 4821 शेयर करें।",
    "lang": "hi"
}

print("Sending request to your AI brain...")

try:
    response = requests.post(url, json=data)
    # Print the nicely formatted JSON response
    print("\n--- AI Response ---")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Failed to connect: {e}")