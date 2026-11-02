# voice-narration

テキストファイルから、日本語・英語のナレーション音声を自動生成する Python スクリプトです。

## できること
- スライドの原稿(テキスト)を1行ずつ音声にして、スライド1枚ごとの mp3 にまとめます
- 日本語は VoiceVox、英語は ElevenLabs を使います

## 使い方
1. VoiceVox のアプリを起動します
2. `.env` ファイルに `ELEVENLABS_API_KEY=(自分のキー)` を書きます
3. 原稿を `slides/slide_1_jp.txt`、`slides/slide_1_en.txt` のように置きます(1行が1つの音声になります)
4. `python slide_jp.py` と `python slide_en.py` を実行します
5. `output/` に、`slide_1_jp.mp3` などができます

## 必要なもの
- Python 3.13
- `pip install requests python-dotenv pydub audioop-lts`
- ffmpeg

## ファイル
- `hello_voice.py`: VoiceVox で、原稿を一括で音声にする最初の版
- `eleven_tts.py`: ElevenLabs で音声を作る最初の版
- `make_narration.py`: 音声ファイルを1本につなぐ
- `slide_jp.py` / `slide_en.py`: スライドごとのナレーションを自動生成する(完成版)

## クレジット
- VOICEVOX:ずんだもん
- 英語音声は ElevenLabs の無料プランで生成しています。商用利用の前に、最新の規約を確認してください