import pyttsx3
import threading

def init_tts():
    engine = pyttsx3.init()  # initialize TTS engine
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)  # adjust index if needed
    engine.setProperty('rate', 150)  # speaking speed
    engine.setProperty('volume', 0.8)  # volume (0.0 to 1.0)
    return engine

def say(engine, text: str = "None"):
    def run_speech():
        engine.say(text)
        engine.iterate()
    # Run in a separate thread
    threading.Thread(target=run_speech, daemon=True).start()