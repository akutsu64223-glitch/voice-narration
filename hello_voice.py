import requests
from pathlib import Path

BASE = "http://localhost:50021"
SPEAKER = 3
SPEED = 1.4
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def make_voice(text, filename):
    # 1. 設計図を作る(audio_query)
    query = requests.post(f"{BASE}/audio_query", params={"text": text, "speaker": SPEAKER})
    query.raise_for_status()
    data = query.json()
    data["speedScale"] = SPEED
    # 2. 設計図から音声を作る(synthesis)
    audio = requests.post(f"{BASE}/synthesis", params={"speaker": SPEAKER}, json=data)
    audio.raise_for_status()
    # 3. wavファイルとして保存する
    with open(filename, "wb") as f:
        f.write(audio.content)
    print(f"{filename}を作りました")

lines = []
with open("lines.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)

for i, line in enumerate(lines, start=1):
    make_voice(line, OUTPUT_DIR / f"voice_{i:02d}.wav")
