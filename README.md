# ASR Fallback Transcription Pipeline
Supports both OpenAI Whisper and local `faster-whisper` transcription.
---
## 🔧 Setup

### 1. Install dependencies
pip install -r requirements.txt
pip install faster-whisper openai flask pytest python-dotenv

Set your OPENAI_API_KEY in .env

Run:
python main.py

Output:
curl -X POST http://127.0.0.1:5000/build_srt_file/1 -F 'file=@hello.wav'

pytest:
PYTHONPATH=. pytest -q tests/test_asr_fallback.py



