"""
RasAssist – Alexa-ähnlicher Sprachassistent
Pipeline: Wake-Word → STT → LLM → TTS
"""

import pyaudio
import yaml
from dotenv import load_dotenv

from rasassist import LLMClient, SpeechToText, TextToSpeech, WakeWordDetector

load_dotenv()

FORMAT = pyaudio.paInt16
CHANNELS = 1
WAKE_CHUNK = 1280  # Pflicht für OpenWakeWord
STT_CHUNK = 1024


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main() -> None:
    config = load_config()
    rate: int = config["audio"]["rate"]

    # Komponenten initialisieren
    wake = WakeWordDetector(
        model_path=config["wake_word"]["model_path"],
        threshold=config["wake_word"]["threshold"],
    )
    stt = SpeechToText(
        model=config["stt"]["model"],
        threshold=config["stt"]["threshold"],
        silence_duration=config["stt"]["silence_duration"],
        rate=rate,
    )
    llm = LLMClient(model=config["llm"]["model"])
    tts = TextToSpeech(voice=config["tts"]["voice"])

    audio = pyaudio.PyAudio()
    print("\n=== RasAssist bereit. Sag 'Hey Raspberry'! ===\n")

    try:
        while True:
            # Phase 1: Wake-Word lauschen
            wake_stream = audio.open(
                format=FORMAT, channels=CHANNELS, rate=rate,
                input=True, frames_per_buffer=WAKE_CHUNK,
            )
            while True:
                data = wake_stream.read(WAKE_CHUNK, exception_on_overflow=False)
                if wake.predict(data):
                    break
            wake_stream.stop_stream()
            wake_stream.close()

            print("[Wake-Word erkannt!]")

            # Phase 2: Sprache aufnehmen & transkribieren
            stt_stream = audio.open(
                format=FORMAT, channels=CHANNELS, rate=rate,
                input=True, frames_per_buffer=STT_CHUNK,
            )
            user_text = stt.transcribe(stt_stream, chunk_size=STT_CHUNK)
            stt_stream.stop_stream()
            stt_stream.close()

            if not user_text:
                continue
            print(f"Du:         {user_text}")

            # Phase 3: LLM-Antwort generieren
            response = llm.ask(user_text)
            print(f"RasAssist:  {response}")

            # Phase 4: Antwort vorlesen
            tts.speak(response)

    except KeyboardInterrupt:
        print("\nBeende RasAssist...")
    finally:
        audio.terminate()


if __name__ == "__main__":
    main()
