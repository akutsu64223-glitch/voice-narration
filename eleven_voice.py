import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.environ["ELEVENLABS_API_KEY"]

BASE = "https://api.elevenlabs.io"
HEADERS = {"xi-api-key": API_KEY}

res = requests.get (f"{BASE}/v1/voices", headers=HEADERS)
res.raise_for_status()
for voice in res.json()["voices"]:
    print(voice["name"], voice["voice_id"])