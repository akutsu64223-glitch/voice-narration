# 1. 部品を読み込む(AudioSegment は pydub から、Path は pathlib から)
from pydub import AudioSegment
from pathlib import Path
# 2. 設定: 無音の長さ GAP_MS = 600、読み込む場所 OUTPUT_DIR
OUTPUT_DIR = Path("output")
GAP_MS = 600
# 3. voice_*.wav を集めて、名前順に並べて files に入れる
files = sorted(OUTPUT_DIR.glob("voice_*.wav"))
files_en = sorted(OUTPUT_DIR.glob("eleven_0*.mp3"))
# 4. 確認: files の中身を for で1つずつ print する
for f in files:
    print(f)
# 5. join_audio(files, out_path) という関数を作る
#    - 空の積み木を作る
#    - files を回して、1つずつ読み込み、「音声 + gap」を足す
#    - out_path に mp3 で書き出す
def join_audio(files, out_path):
    narration = AudioSegment.silent(duration=0)
    gap = AudioSegment.silent(duration=GAP_MS)
    for f in files:
        audio = AudioSegment.from_mp3(f) if f.suffix == ".mp3" else AudioSegment.from_wav(f)
        narration += audio + gap
    narration.export(out_path, format="mp3")
# 6. 日本語版と英語版を、関数の呼び出しで作る
#    narration_jp.mp3 と narration_en.mp3
join_audio(files, OUTPUT_DIR / "narration_jp.mp3")
join_audio(files_en, OUTPUT_DIR / "narration_en.mp3")