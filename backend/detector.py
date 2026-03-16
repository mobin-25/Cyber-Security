scam_words = [
    "otp",
    "urgent",
    "account blocked",
    "account will be blocked",
    "verify your account",
    "verify account",
    "kyc update",
    "share otp"
]
def detect_scam(text):

    detected = []

    for word in scam_words:
        if word in text.lower():
            detected.append(word)

    if len(detected) >= 3:
        risk = "HIGH"
    elif len(detected) >= 1:
        risk = "SUSPICIOUS"
    else:
        risk = "SAFE"

    return risk, detected