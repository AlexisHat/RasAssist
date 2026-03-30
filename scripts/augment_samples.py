"""
Samples vervielfachen und in den OpenWakeWord Trainingsordner kopieren.
Ausführen: python scripts/augment_samples.py
"""

import os
import shutil

SOURCE_DIR = "my_samples"
TARGET_DIR = "openwakeword/audio_data/positive"
MULTIPLIER = 5

os.makedirs(TARGET_DIR, exist_ok=True)

if not os.path.exists(SOURCE_DIR):
    print(f"Fehler: '{SOURCE_DIR}' nicht gefunden.")
    raise SystemExit(1)

files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".wav")]
print(f"Gefundene Samples: {len(files)}")

copy_count = 0
for filename in files:
    for i in range(MULTIPLIER):
        new_name = f"multiplied_{i}_{filename}"
        shutil.copy(
            os.path.join(SOURCE_DIR, filename),
            os.path.join(TARGET_DIR, new_name),
        )
        copy_count += 1

print(f"Fertig: {len(files)} Originale → {copy_count} Dateien in '{TARGET_DIR}'.")
