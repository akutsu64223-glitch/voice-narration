import requests
import os 
from dotenv import load_dotenv 
from pathlib import Path
from pydub import AudioSegment

load_dotenv()
API_KEY = os.environ["ELEVENLABS_API_KEY"]

BASE = "https://api.elevenlabs.io"
HEADERS = {"xi-api-key": API_KEY}
VOICE_ID = "XrExE9yKIg1WjnnlVkGX"
MODEL_ID = "eleven_multilingual_v2"
GAP_MS = 600
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
PARTS_DIR = Path("parts")
PARTS_DIR.mkdir(exist_ok=True)
SLIDES_DIR = Path("slides")

def make_voice(text, filename):
    res = requests.post(
        f"{BASE}/v1/text-to-speech/{VOICE_ID}",
        headers=HEADERS,
        json={"text": text, "model_id": MODEL_ID},
    )
    res.raise_for_status()

    with open(filename, "wb") as f:
        f.write(res.content)
    print(f"{filename}を作りました")
    
def join_audio(files, out_path):
    narration = AudioSegment.silent(duration=0)
    gap = AudioSegment.silent(duration=GAP_MS)
    for f in files:
        audio = AudioSegment.from_mp3(f) if f.suffix == ".mp3" else AudioSegment.from_wav(f)
        narration += audio + gap
    narration.export(out_path, format="mp3")
    
def read_lines(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: 
                lines.append(line)
    return lines

for n in range(1,4):
        lines = read_lines(SLIDES_DIR / f"slide_{n}_en.txt")
        wav_files = []
        for i, line in enumerate(lines, start=1):
            path = PARTS_DIR / f"slide{n}_{i:02d}_en.mp3"
            make_voice(line, path)
            wav_files.append(path)
        join_audio(wav_files, OUTPUT_DIR / f"slide_{n}_en.mp3")