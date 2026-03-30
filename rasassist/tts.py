import os
import platform
import subprocess
import wave

from huggingface_hub import hf_hub_download
from piper.voice import PiperVoice

REPO_ID = "rhasspy/piper-voices"

VOICE_PATHS: dict[str, str] = {
    "thorsten_medium": "de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
    "thorsten_emotional": "de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx",
    "pavoque_low": "de/de_DE/pavoque/low/de_DE-pavoque-low.onnx",
    "karlsson_low": "de/de_DE/karlsson/low/de_DE-karlsson-low.onnx",
    "kerstin_low": "de/de_DE/kerstin/low/de_DE-kerstin-low.onnx",
    "ramona_low": "de/de_DE/ramona/low/de_DE-ramona-low.onnx",
}


class TextToSpeech:
    """Synthetisiert Text zu Sprache mit einem deutschen Piper-Modell."""

    def __init__(self, voice: str = "thorsten_medium"):
        if voice not in VOICE_PATHS:
            raise ValueError(
                f"Stimme '{voice}' unbekannt. "
                f"Verfügbar: {list(VOICE_PATHS.keys())}"
            )
        voice_path = VOICE_PATHS[voice]
        print(f"Lade TTS-Stimme '{voice}'...")
        onnx_path = hf_hub_download(repo_id=REPO_ID, filename=voice_path)
        config_path = hf_hub_download(repo_id=REPO_ID, filename=voice_path + ".json")
        self._voice = PiperVoice.load(onnx_path, config_path)

    def speak(self, text: str, output_path: str = "/tmp/rasassist_tts.wav") -> None:
        """Synthetisiert `text` und spielt die Ausgabe direkt ab."""
        with wave.open(output_path, "wb") as wav_file:
            self._voice.synthesize(text, wav_file)
        player = "afplay" if platform.system() == "Darwin" else "aplay"
        subprocess.run([player, output_path], check=False)
