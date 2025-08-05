import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from faster_whisper import WhisperModel
from tempfile import NamedTemporaryFile

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_PROVIDER = os.getenv("WHISPER_PROVIDER", "auto").lower()

if WHISPER_PROVIDER != "faster-whisper" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment and required for OpenAI mode.")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def get_whisper_srt(filename, file_obj):
    if WHISPER_PROVIDER == "openai":
        return use_openai_whisper(file_obj)
    elif WHISPER_PROVIDER == "faster-whisper":
        return use_local_whisper(file_obj)
    else:  
        try:
            return use_openai_whisper(file_obj)
        except Exception as e:
            print("OpenAI failed, falling back to local:", e)
            return use_local_whisper(file_obj)

def use_openai_whisper(file_obj):
    file_obj.seek(0)
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=file_obj,
        response_format="verbose_json"
    )
    print("OpenAI response:", response)
    return response

def use_local_whisper(file_obj):
    file_obj.seek(0)
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(file_obj.read())
        temp_audio.flush()

        model = WhisperModel("base", compute_type="float32")

        result = model.transcribe(temp_audio.name, language="en")
        print("DEBUG: transcribe() returned:", result)

        if result is None:
            raise ValueError("WhisperModel.transcribe returned None")

        segments = None
        if isinstance(result, tuple) and len(result) == 2:
            segments = result[0]
        elif hasattr(result, '__iter__'):
            segments = result
        else:
            raise ValueError(f"Unexpected transcribe() return type: {type(result)}")

        if segments is None:
            raise ValueError("No segments found from transcribe()")

        segments_list = []
        for i, segment in enumerate(segments):
            seg_words = []

            words = getattr(segment, "words", []) or []
            for word_info in words:
                seg_words.append({
                    "start": word_info.start,
                    "end": word_info.end,
                    "word": word_info.word
                })
            segments_list.append({
                "id": i,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": seg_words,
            })

        result_dict = {
            "text": " ".join([seg["text"] for seg in segments_list]),
            "segments": segments_list,
        }
        return result_dict
