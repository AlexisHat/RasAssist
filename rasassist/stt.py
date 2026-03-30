import numpy as np
import torch
import whisper


class SpeechToText:
    """Transkribiert Sprache aus einem Audio-Stream mittels Whisper."""

    def __init__(
        self,
        model: str = "small",
        threshold: float = 0.02,
        silence_duration: float = 1.5,
        rate: int = 16000,
    ):
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.rate = rate

        print(f"Lade Whisper-Modell '{model}'...")
        self._model = whisper.load_model(model)

    def transcribe(self, stream, chunk_size: int = 1024) -> str:
        """
        Liest aus `stream` bis Stille erkannt wird, dann Transkription.
        Gibt den transkribierten Text zurück.
        """
        audio_buffer = []
        is_speaking = False
        silence_counter = 0.0

        print(">>> Höre zu...")
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            amplitude = float(np.sqrt(np.mean(chunk ** 2)))

            if amplitude > self.threshold:
                if not is_speaking:
                    print(">>> Aufnahme läuft...")
                is_speaking = True
                silence_counter = 0.0
                audio_buffer.append(data)
            elif is_speaking:
                audio_buffer.append(data)
                silence_counter += chunk_size / self.rate

                if silence_counter > self.silence_duration:
                    print("--- Transkribiere...")
                    full_audio = b"".join(audio_buffer)
                    audio_np = (
                        np.frombuffer(full_audio, dtype=np.int16).astype(np.float32)
                        / 32768.0
                    )
                    result = self._model.transcribe(
                        audio_np, fp16=torch.cuda.is_available()
                    )
                    return result["text"].strip()
