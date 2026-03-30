"""
Alle verfügbaren deutschen Piper-Stimmen vergleichen.
Ausführen: python scripts/test_voices.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import wave
from rasassist.tts import REPO_ID, VOICE_PATHS, TextToSpeech

TEST_TEXT = "Das ist ein automatischer Test. Hallo, ich bin dein Sprachassistent."

for name in VOICE_PATHS:
    print(f"\n--- Teste Stimme: {name} ---")
    try:
        tts = TextToSpeech(voice=name)
        tts.speak(TEST_TEXT, output_path=f"test_{name}.wav")
        print(f"OK: test_{name}.wav")
    except Exception as e:
        print(f"Fehler bei '{name}': {e}")
