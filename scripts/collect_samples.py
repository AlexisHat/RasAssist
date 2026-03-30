"""
Wake-Word Samples aufnehmen.
Ausführen: python scripts/collect_samples.py
"""

import os

import sounddevice as sd
from scipy.io import wavfile

SAMPLE_RATE = 16000
DURATION = 2  # Sekunden pro Aufnahme
OUTPUT_DIR = "my_samples"

os.makedirs(OUTPUT_DIR, exist_ok=True)
print("Starte Aufnahme-Session...")
print("Drücke STRG+C zum Beenden.\n")

try:
    count = 0
    while True:
        count += 1
        input(f"[{count}] Drücke ENTER, sag 'Hey Raspberry' und warte kurz...")
        recording = sd.rec(
            int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16"
        )
        sd.wait()
        filename = os.path.join(OUTPUT_DIR, f"sample_{count}.wav")
        wavfile.write(filename, SAMPLE_RATE, recording)
        print(f"  Gespeichert: {filename}")
except KeyboardInterrupt:
    print("\nSession beendet.")
