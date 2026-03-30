# RasAssist

Ein lokaler, deutschsprachiger Sprachassistent für den Raspberry Pi — gebaut wie Alexa, aber vollständig selbst gehostet.

## Pipeline

```
Mikrofon → Wake-Word-Erkennung → Spracherkennung → LLM → Text-to-Speech → Lautsprecher
```

1. **Wake-Word** – OpenWakeWord erkennt "Hey Raspberry" lokal per ONNX-Modell
2. **STT** – OpenAI Whisper transkribiert die Spracheingabe auf Deutsch
3. **LLM** – OpenRouter leitet die Anfrage an ein kostenloses Sprachmodell weiter
4. **TTS** – Piper synthetisiert die Antwort mit einer deutschen Stimme

## Projektstruktur

```
RasAssist/
├── main.py                   # Einstiegspunkt, orchestriert die gesamte Pipeline
├── config.yaml               # Alle Einstellungen zentral
├── requirements.txt
│
├── rasassist/                # Kern-Paket
│   ├── wake_word.py          # WakeWordDetector  (OpenWakeWord)
│   ├── stt.py                # SpeechToText      (Whisper)
│   ├── llm.py                # LLMClient         (OpenRouter)
│   └── tts.py                # TextToSpeech      (Piper)
│
├── scripts/
│   ├── collect_samples.py    # Wake-Word-Samples aufnehmen
│   ├── augment_samples.py    # Samples für das Training vervielfachen
│   └── test_voices.py        # Alle Piper-Stimmen vergleichen
│
├── training/
│   └── automatic_model_training.ipynb  # Wake-Word-Modell trainieren
│
└── models/                   # Trainierte ONNX-Modelle
```

## Setup

### 1. Abhängigkeiten installieren

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API-Key konfigurieren

```bash
cp .env.example .env
```

`.env` öffnen und den OpenRouter-Key eintragen:

```
OPENROUTER_API_KEY=sk-or-...
```

Kostenloser Account: [openrouter.ai](https://openrouter.ai)

### 3. Starten

```bash
python main.py
```

## Konfiguration

Alle Parameter in `config.yaml` anpassen:

```yaml
wake_word:
  model_path: models/hey_razz_py.onnx
  threshold: 0.20        # Empfindlichkeit (0.0–1.0)

stt:
  model: small           # tiny | base | small | medium | large
  silence_duration: 1.5  # Sekunden Stille bis Transkription startet

tts:
  voice: thorsten_medium # Siehe verfügbare Stimmen unten

llm:
  model: meta-llama/llama-3.3-70b-instruct:free
```

### Verfügbare TTS-Stimmen

| Name | Qualität |
|---|---|
| `thorsten_medium` | Empfohlen – natürlich klingend |
| `thorsten_emotional` | Emotionaler Ausdruck |
| `pavoque_low` | Leichtere Stimme |
| `karlsson_low` | Alternativstimme |
| `kerstin_low` | Weiblich |
| `ramona_low` | Weiblich |

Stimmen vergleichen:
```bash
python scripts/test_voices.py
```

### Empfohlene kostenlose LLM-Modelle (OpenRouter)

| Modell | Eigenschaft |
|---|---|
| `meta-llama/llama-3.3-70b-instruct:free` | Standard, schnell |
| `deepseek/deepseek-chat:free` | Sehr stark (DeepSeek V3) |
| `deepseek/deepseek-r1:free` | Reasoning, langsamer |

## Eigenes Wake-Word trainieren

### Samples aufnehmen

```bash
python scripts/collect_samples.py
```

### Samples vervielfachen (Datenmenge erhöhen)

```bash
python scripts/augment_samples.py
```

### Modell trainieren

Das Notebook `training/automatic_model_training.ipynb` führt durch den vollständigen Trainingsprozess mit OpenWakeWord (empfohlen: Google Colab für GPU-Beschleunigung).

Das trainierte `.onnx`-Modell dann in `models/` ablegen und den Pfad in `config.yaml` aktualisieren.

## Abhängigkeiten

| Bibliothek | Zweck |
|---|---|
| `openwakeword` | Wake-Word-Erkennung |
| `openai-whisper` | Spracherkennung |
| `piper-tts` | Text-to-Speech |
| `openai` | OpenRouter-Client |
| `pyaudio` | Audio-Stream |
