from gtts import gTTS
import tempfile

def synthesize(text: str, format: str = "mp3"):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tts.save(f"{fp.name}.{format}")
        return f"{fp.name}.{format}" 