import requests
import os

key = os.environ.get("GEMINI_API_KEY", "")
print(f"Key loaded: {key[:8]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={key}"
r = requests.post(url, json={"contents": [{"parts": [{"text": "say hello"}]}]})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")
