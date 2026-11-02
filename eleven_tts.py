#1.部品を読み込む
import os 
import requests
from dotenv import load_dotenv
from pathlib import Path

#2. .env からキーを読み込む
load_dotenv()
API_KEY = os.environ["ELEVENLABS_API_KEY"]

#3. 定数を決める
BASE = "https://api.elevenlabs.io"
HEADERS = {"xi-api-key": API_KEY}
VOICE_ID = "XrExE9yKIg1WjnnlVkGX"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
print("準備OK", len(API_KEY))

#4. 読ませる英語を用意させる
TEXT = "Hello. This is a distance synthesizer. It measures the distance to your hand with an ultrasonic sensor."

def make_voice(text, filename):
    #5. 音声を作る
    res = requests.post(
        f"{BASE}/v1/text-to-speech/{VOICE_ID}",
        headers=HEADERS,
        json={"text": text, "model_id": MODEL_ID},
    )

    #6. エラーなら止める
    res.raise_for_status()

    #7. output フォルダに eleven_test.mp3として "wb" で保存する
    with open(filename, "wb") as f:
        f.write(res.content)
    print(f"{filename}を作りました")

#8. lines_en.txt を読んで、空行を除いてlinesに入れる
lines = []
with open("lines_en.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)
#9. for と enumurate で、1行ずつ make_voice() を呼ぶ
for i, line in enumerate(lines, start=1):
    make_voice(line, OUTPUT_DIR / f"eleven_{i:02d}.mp3")