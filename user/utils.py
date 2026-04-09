import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_otp():
    return str(random.randint(100000, 999999))



BREVO_API_KEY = os.getenv("BREVO_API_KEY")

def send_otp_email(email, otp):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {"name": "Lex-Todo", "email": "amadiamos146@gmail.com"},
        "to": [{"email": email}],
        "subject": "Email Verification OTP",
        "htmlContent": f"<p>Your OTP is <b>{otp}</b></p>"
    }

    response = requests.post(url, json=data, headers=headers)

    return response.json()