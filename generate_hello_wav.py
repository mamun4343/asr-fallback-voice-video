from gtts import gTTS
from pydub import AudioSegment

text = "Hello world"
tts = gTTS(text=text, lang='en', slow=False)
tts.save("temp.mp3")

audio = AudioSegment.from_mp3("temp.mp3")
audio.export("hello.wav", format="wav")

print("Generated hello.wav with speech.")

