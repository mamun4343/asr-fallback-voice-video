
import os
import pytest
from unittest.mock import patch
from src.utils.video_utils import get_whisper_srt

@pytest.fixture
def sample_audio():
    return b"FAKE_AUDIO_BYTES"

@pytest.fixture
def fake_result():
    return {
        "text": "Hello world",
        "segments": [
            {
                "id": 0,
                "start": 0.0,
                "end": 1.5,
                "text": "Hello world",
                "words": [
                    {"start": 0.0, "end": 0.5, "word": "Hello"},
                    {"start": 0.6, "end": 1.5, "word": "world"},
                ],
            }
        ]
    }

def test_adapter_structure(fake_result):
    assert "text" in fake_result
    assert isinstance(fake_result["segments"], list)
    assert "words" in fake_result["segments"][0]


@patch("src.utils.video_utils.use_local_whisper")
def test_faster_whisper_flow(mock_transcribe, sample_audio, fake_result):
    os.environ["WHISPER_PROVIDER"] = "faster-whisper"
    mock_transcribe.return_value = fake_result

    result = get_whisper_srt("hello.wav", sample_audio)
    assert result["text"] == "Hello world"
    assert result["segments"][0]["text"] == "Hello world"








