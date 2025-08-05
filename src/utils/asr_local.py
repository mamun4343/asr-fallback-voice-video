from faster_whisper import WhisperModel

def transcribe_local(audio_bytes: bytes, language: str = None) -> dict:
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_bytes, language=language, word_timestamps=True)

    result = {
        "text": "",
        "segments": []
    }

    for idx, segment in enumerate(segments):
        words = [{
            "start": word.start,
            "end": word.end,
            "word": word.word.strip()
        } for word in segment.words if word.word.strip()]

        result["segments"].append({
            "id": idx,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "words": words
        })

        result["text"] += segment.text.strip() + " "

    result["text"] = result["text"].strip()
    return result




