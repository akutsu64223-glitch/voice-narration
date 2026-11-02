# 1. 部品を読み込む(requests、Path、AudioSegment)
import requests 
from pathlib import Path
from pydub import AudioSegment
# 2. 設定: BASE、SPEAKER、SPEED、GAP_MS、OUTPUT_DIR、SLIDES_DIR
#    SLIDES_DIR は Path("slides")
BASE = "http://localhost:50021"
SPEAKER = 3
SPEED = 1.4
GAP_MS = 600
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
PARTS_DIR = Path("parts")
PARTS_DIR.mkdir(exist_ok=True)
SLIDES_DIR = Path("slides")
# 3. make_voice(text, filename) ── hello_voice.py からコピー
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
# 4. join_audio(files, out_path) ── make_narration.py からコピー
def join_audio(files, out_path):
    narration = AudioSegment.silent(duration=0)
    gap = AudioSegment.silent(duration=GAP_MS)
    for f in files:
        audio = AudioSegment.from_mp3(f) if f.suffix == ".mp3" else AudioSegment.from_wav(f)
        narration += audio + gap
    narration.export(out_path, format="mp3")
# 5. read_lines(path) ── ファイルを読んで、空行を除いた行のリストを返す
def read_lines(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: 
                lines.append(line)
    return lines
# 6. スライド1〜3を順に処理する
#    for n in ...:
for n in range(1,4):
#      a. read_lines で slides/slide_{n}_jp.txt を読む
        lines = read_lines(SLIDES_DIR / f"slide_{n}_jp.txt")
#      b. 行ごとに make_voice で wav を作り、パスをリストにためる
#         保存先: output/slide{n}_{i:02d}.wav
        wav_files = []
        for i, line in enumerate(lines, start=1):
            path = PARTS_DIR / f"slide{n}_{i:02d}.wav"
            make_voice(line, path)
            wav_files.append(path)
#      c. ためたリストを join_audio で1本にする
#         出力: output/slide_{n}_jp.mp3
        join_audio(wav_files, OUTPUT_DIR / f"slide_{n}_jp.mp3")